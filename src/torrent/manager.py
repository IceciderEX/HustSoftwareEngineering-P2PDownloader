import math
import os
from typing import List

from torrent import Torrent
from piece import *
from message import REQUEST_SIZE


class PieceManager:
    def __init__(self, torrent: Torrent):
        self.torrent = torrent
        self.peers = {}
        self.pending_blocks = []
        self.missing_pieces = []
        self.ongoing_pieces = []
        self.have_pieces = []
        self.max_pending_time = 300 * 1000  # 5分钟
        self.missing_pieces = None
        self.total_pieces = len(torrent.pieces)
        self.fd = os.open(self.torrent.name, os.O_RDWR | os.O_CREAT)  # 在当前目录下创建下载的文件

    def _init_pieces(self) -> List[Piece]:
        """
        使用torrent数据初始化每一个Piece和包含的Block
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
        if self.fd:
            os.close(self.fd)

    def finished(self) -> bool:
        return len(self.have_pieces) == self.total_pieces

    def bytes_downloaded(self) -> int:
        return len(self.have_pieces) * self.torrent.piece_length

    def add_peer(self, peer_id, bitfield):
        self.peers[peer_id] = bitfield

    def update_peer(self, peer_id, index: int):
        if peer_id in self.peers:
            self.peers[peer_id][index] = 1

    def remove_peer(self, peer_id):
        if peer_id in self.peers:
            del self.peers[peer_id]
