# @author 郑卯杨
# @date 2023/9/30
# @description 实现了Block类和Piece类,保存向Peer结点请求的数据

import logging
from hashlib import sha1
from typing import Optional


class Block:
    """
    Block 是 Piece的一部分,每次向Peer请求的是Block大小的数据
    除了每个Piece的最后一个Block外,都是REQUEST_SIZE(2**14)
    """
    Missing = 0
    Pending = 1
    Retrieved = 2

    def __init__(self, piece: int, offset: int, length: int):
        """
        :param piece: 属于哪一个piece
        :param offset: 在piece中的偏移
        :param length: 数据长度
        """
        self.piece = piece
        self.offset = offset
        self.length = length
        self.status = Block.Missing
        self.data = None


class Piece:
    def __init__(self, index: int, blocks: [], hash_value):
        """
        :param index: 在整个文件中的index
        :param blocks: 被划分的所有block
        :param hash_value: 所有数据一起使用sha1计算出的hash,用于核对信息
        """
        self.index = index
        self.blocks = blocks
        self.hash = hash_value

    def reset(self) -> None:
        for block in self.blocks:
            block.status = Block.Missing

    def next_request(self) -> Optional[Block]:
        """
        :return: 返回第一个缺失的Block
        """
        missing = [b for b in self.blocks if b.status is Block.Missing]
        if missing:
            missing[0].status = Block.Pending
            return missing[0]
        return None

    def block_received(self, offset: int, data: bytes):
        match = [b for b in self.blocks if b.offset == offset]
        block = match[0] if match else None
        if block:
            block.status = Block.Retrieved
            block.data = data
        else:
            logging.warning(f"Trying to receive a non-existing block {offset=}")

    def finished(self) -> bool:
        blocks = [b for b in self.blocks if b.status is not Block.Retrieved]
        return len(blocks) == 0

    @property
    def data(self):
        """
        :return:所有block的数据按顺序合在一起就是piece.data
        """
        total = sorted(self.blocks, key=lambda b: b.offset)
        return b''.join([b.data for b in total])

    def match(self) -> bool:
        piece_hash = sha1(self.data).digest()
        return piece_hash == self.hash
