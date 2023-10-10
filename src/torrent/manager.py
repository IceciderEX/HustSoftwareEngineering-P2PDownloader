import math
import os
import time
from collections import defaultdict
from typing import List, Dict
from bitstring import BitArray
from src.torrent.torrent import Torrent
from src.torrent.piece import *
from src.torrent.message import REQUEST_SIZE

"""
    @filename manager.py
    @author 郑卯杨
    @date 2023/10/10
    @version 1.0

    该模块实现了PieceManager,负责管理向Peer请求Piece对应的数据,接受数据,写回数据
"""


class PendingRequest:
    """
    对需要请求的BLock进行封装,额外添加了定时器信息
    """

    def __init__(self, block, added):
        self.block = block
        self.added = added


class PieceManager:
    """
    对Piece进行管理,负责决定请求块数据,写回Piece数据
    """

    def __init__(self, torrent: Torrent):
        self.torrent = torrent
        self.peers: Dict[bytes, BitArray] = {}
        self.pending_blocks: List[PendingRequest] = []
        self.missing_pieces: List[Piece] = []
        self.ongoing_pieces: List[Piece] = []
        self.have_pieces: List[Piece] = []
        self.max_pending_time = 120  # 2分钟
        self.total_pieces = len(torrent.pieces)
        self.fd = os.open(self.torrent.name, os.O_RDWR | os.O_CREAT)  # 在当前目录下创建下载的文件
        self.missing_pieces: List[Piece] = self._init_pieces()

    def _init_pieces(self) -> List[Piece]:
        """使用torrent数据初始化每一个Piece和其包含的Block,只有最后一个piece的最后一个block可能不是标准大小

        :return: List[Piece]
        """
        pieces = []
        std_num_blocks = math.ceil(self.torrent.piece_length / REQUEST_SIZE)

        for index, hash_value in enumerate(self.torrent.pieces):
            if index < (self.total_pieces - 1):
                blocks = [Block(index, offset * REQUEST_SIZE, REQUEST_SIZE)
                          for offset in range(std_num_blocks)]
            else:
                last_piece_len = self.torrent.length % self.torrent.piece_length
                num_blocks = math.ceil(last_piece_len / REQUEST_SIZE)
                blocks = [Block(index, offset * REQUEST_SIZE, REQUEST_SIZE)
                          for offset in range(num_blocks)]
                if last_piece_len % REQUEST_SIZE > 0:
                    blocks[-1].length = last_piece_len % REQUEST_SIZE
            pieces.append(Piece(index, blocks, hash_value))
        return pieces

    def close(self) -> None:
        """
        关闭对应的文件描述符
        """
        if self.fd:
            os.close(self.fd)

    @property
    def finished(self) -> bool:
        """
        :return: 所有的Piece是否都被下载
        """
        return len(self.have_pieces) == self.total_pieces

    @property
    def bytes_downloaded(self) -> int:
        """
        :return: 下载的bytes数
        """
        return len(self.have_pieces) * self.torrent.piece_length

    def add_peer(self, peer_id: bytes, bitfield):
        """
        :param peer_id: 标识 Peer
        :param bitfield: bitmap
        :return: 加入peer对应的piece bitmap
        """
        self.peers[peer_id] = bitfield

    def update_peer(self, peer_id: bytes, index: int) -> None:
        """将Peer拥有的第index个piece标识为1

        :param peer_id: 标识 Peer
        :param index: Piece的序号
        """
        if peer_id in self.peers:
            self.peers[peer_id][index] = 1

    def remove_peer(self, peer_id: bytes) -> None:
        """移除Peer

        :param peer_id: 标识 Peer
        """
        if peer_id in self.peers:
            del self.peers[peer_id]

    def _expired_requests(self, peer_id: bytes) -> Optional[Block]:
        """
        :return: 如果Block请求时间超过了max_pending_time,需要被重新请求
        """
        current = round(time.time())
        for request in self.pending_blocks:
            if self.peers[peer_id][request.block.piece]:
                if request.added + self.max_pending_time < current:
                    logging.info(f"Re-requesting block {request.block.offset} for piece {request.block.piece}")
                    request.added = current
                    return request.block
        return None

    def _next_ongoing(self, peer_id: bytes) -> Optional[Block]:
        """
        寻找peer对应的ongoing队列中,第一个可以请求的piece,将其中第一个可以请求的block加入pending_blocks
        """
        for piece in self.ongoing_pieces:
            if self.peers[peer_id][piece.index]:
                block = piece.next_request()
                if block:
                    self.pending_blocks.append(PendingRequest(block, round(time.time())))
                    return block
        return None

    def _get_rarest_piece(self, peer_id: bytes) -> Optional[Piece]:
        """
        寻找所有peer中拥有的最少的piece,最先请求
        """
        piece_count = defaultdict(int)
        for piece in self.missing_pieces:
            if not self.peers[peer_id][piece.index]:
                # 如果peer没有该piece
                continue
            for p in self.peers:
                if self.peers[p][piece.index]:
                    piece_count[piece] += 1
        if piece_count:
            rarest_piece: Piece = min(piece_count, key=lambda p: piece_count[p])
            self.missing_pieces.remove(rarest_piece)
            self.ongoing_pieces.append(rarest_piece)
            return rarest_piece
        return None

    def _next_missing_block(self, peer_id: bytes) -> Optional[Block]:
        for index, piece in enumerate(self.missing_pieces):
            if self.peers[peer_id][piece.index]:
                piece = self.missing_pieces.pop(index)
                self.ongoing_pieces.append(piece)
                return piece.next_request()
        return None

    def _write(self, piece) -> None:
        """将一个Piece对应的全部数据写到文件

        :param piece: Piece
        """
        pos = piece.index * self.torrent.piece_length
        os.lseek(self.fd, pos, os.SEEK_SET)
        os.write(self.fd, piece.data)

    def next_request(self, peer_id: bytes) -> Optional[Block]:
        """

        block的请求优先级如下:
        1.在请求队列中,请求超时的block,重新请求
        2.请求ongoing队列中的piece缺少的block
        3.将缺失的piece加入ongoing队列,并请求其缺少的block

        :return: 符合条件的Block 或 None
        """

        if peer_id not in self.peers:
            return None
        block = self._expired_requests(peer_id)
        if not block:
            block = self._next_ongoing(peer_id)
            if not block:
                rarest_piece = self._get_rarest_piece(peer_id)
                if rarest_piece:
                    block = rarest_piece.next_request()
        return block

    def block_received(self, peer_id: bytes, piece_index: int, block_offset: int, data: bytes) -> None:
        """接受Block数据,如果一个Piece的全部数据都被接受,写回到文件

        :param peer_id: Peer 标识
        :param piece_index: piece在torrent文件的index
        :param block_offset: block在piece中的偏移量
        :param data: 请求的block数据
        """

        logging.debug(f"Received block {block_offset} for piece {piece_index} from peer {peer_id}: ")
        for index, request in enumerate(self.pending_blocks):
            if request.block.piece == piece_index and request.block.offset == block_offset:
                del self.pending_blocks[index]
                break

        pieces = [p for p in self.ongoing_pieces if p.index == piece_index]
        piece = pieces[0] if pieces else None
        if piece:
            piece.block_received(block_offset, data)
            if piece.finished():
                if piece.match():
                    self._write(piece)
                    self.ongoing_pieces.remove(piece)
                    self.have_pieces.append(piece)
                    logging.info(
                        f"{len(self.have_pieces)} / {self.total_pieces} pieces download "
                        f"{(len(self.have_pieces) / self.total_pieces * 100):.3f} %")
                else:
                    # piece hash 不匹配,必须重新请求
                    logging.info(f"piece {piece.index} corrupt")
                    piece.reset()
        else:
            logging.warning("Trying to update piece that is not ongoing")

    def download_progress(self):
        """
            下载速率接口
        """
        return len(self.have_pieces) / (self.total_pieces * 100)
