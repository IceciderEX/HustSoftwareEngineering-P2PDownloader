import hashlib

import bencodepy
import binascii
import libtorrent

import MagnetlinkParser
from src.torrent import bencoding
from src.torrent import torrent
from src.torrent.torrent import Torrent


class TorrentNoFile:
    def __init__(self, info_hash, display_name, trackers):
        self.info_hash = info_hash
        self.display_name = display_name
        self.trackers = trackers

    def to_dict(self):
        return {
            'info': {
                'name': self.display_name,
                'pieces': '',
                'piece length': 0,
                'length': 0
            },
            'info_hash': self.info_hash,
            'display_name': self.display_name,
            'trackers': self.trackers
        }


"""
将磁力链接转换为torrent文件
由于不知道怎么导入libtorrent库，暂时无法完成
"""
def transform_link_to_torrent(link, output_torrent_file):
    mag_parser = MagnetlinkParser.magnetlinkParser(link)
    meta_info = mag_parser.parse_magnetlink()
    torrent = TorrentNoFile(meta_info.info_hash, meta_info.display_name, meta_info.trackers)
    torrent_data = torrent.to_dict()
    info_hash_str = torrent_data['info_hash']
    print(info_hash_str)
    info_hash_bytes = binascii.unhexlify(info_hash_str)
    print(info_hash_bytes)
    info_dict = bencodepy.decode_dict(info_hash_bytes)

    file = open(output_torrent_file, "wb")
    file.write(bencodepy.encode(torrent_data))


transform_link_to_torrent("magnet:?xt=urn:btih:4225824a42f4afceec51cf73ae85fdc76f14aebd&dn=Mind.Games.rar&tr=udp%3a"
                          "%2f%2ftracker.torrent.eu.org%3a451%2fannounce&tr=udp%3a%2f%2fexodus.desync.com%3a6969"
                          "%2fannounce&tr=udp%3a%2f%2ftracker.moeking.me%3a6969%2fannounce", "D:\\output.torrent")
