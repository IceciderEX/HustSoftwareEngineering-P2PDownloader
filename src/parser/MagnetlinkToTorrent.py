import bencodepy
import MagnetlinkParser


class Torrent:
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


def transform_link_to_torrent(link, output_torrent_file):
    parsed_data = MagnetlinkParser.magnetlinkParser.parse_magnetlink(link)
    torrent = Torrent(parsed_data.info_hash, parsed_data.display_name, parsed_data.trackers)
    torrent_data = torrent.to_dict()

    file = open(output_torrent_file, "wb")
    file.write(bencodepy.encode(torrent_data))
