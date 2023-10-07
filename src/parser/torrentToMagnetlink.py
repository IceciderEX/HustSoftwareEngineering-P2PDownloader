import bencodepy
from ..torrent.torrent import Torrent


class toMagnetlink:
    def __init__(self, filepath: str):
        torrent = Torrent(filepath)
        info_hash = torrent.info_hash
        file_name = torrent.meta_info['name']
        file_comment = torrent.meta_info['comment']
        trackers = torrent.meta_info['announce']

