import logging
import re
import asyncio

class magnetLink:
    def __init__(self, link, info_hash, display_name, trackers):
        self.link = link
        self.info_hash = info_hash
        self.display_name = display_name
        self.trackers = trackers

    def read_from_file(self, file_path: str):
        f = open(file_path, "r")
        meta_info = f.read()
        parsed_link = magnetlinkParser(meta_info).parse_magnetlink()
        self.link = parsed_link.link
        self.info_hash = parsed_link.info_hash
        self.display_name = parsed_link.display_name
        self.trackers = parsed_link.trackers

    def generate_mag_link(self):
        mag_link = "magnet:?xt=urn:btih:"
        mag_link += str(self.info_hash)
        mag_link += ("&dn=" + str(self.display_name))
        for tracker in self.trackers:
            mag_link += "&tr="
            mag_link += tracker
        logging.info("Generate magnet link file successfully!")
        return mag_link


class magnetlinkParser:
    magnetlink = ""

    def __init__(self, magnetlink):
        self.magnetlink = magnetlink

    def parse_magnetlink(self):
        info_hash = ""
        display_name = ""
        trackers = []

        # Update the pattern to handle infohash only
        pattern = r"magnet:\?xt=urn:btih:([^&]+)(?:&dn=([^&]+))?(?:&tr=([^&]+(?:&tr=[^&]+)*))?"

        match = re.match(pattern, self.magnetlink)
        if match:
            info_hash = match.group(1)
            display_name = match.group(2) if match.group(2) else ""
            trackers = match.group(3).split("&tr=") if match.group(3) else []

        return magnetLink(link=self.magnetlink, info_hash=info_hash, display_name=display_name, trackers=trackers)


# link_str = ("magnet:?xt=urn:btih:4225824a42f4afceec51cf73ae85fdc76f14aebd&dn=Mind.Games.rar&tr=udp%3a%2f%2ftracker.torrent"
#       ".eu.org%3a451%2fannounce&tr=udp%3a%2f%2fexodus.desync.com%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.moeking.me"
#       "%3a6969%2fannounce")
# link_to_parse = magnetlinkParser(link_str).parse_magnetlink()
#
# print(link_to_parse.info_hash)
# print(link_to_parse.trackers)
# print(link_to_parse.display_name)
#
# link = magnetLink(link_str, link_to_parse.info_hash, link_to_parse.display_name, link_to_parse.trackers)
# mag_link = link.generate_mag_link()
# print(mag_link)
# print("magnet:?xt=urn:btih:4225824a42f4afceec51cf73ae85fdc76f14aebd&dn=Mind.Games.rar&tr=udp%3a%2f%2ftracker.torrent"
#       ".eu.org%3a451%2fannounce&tr=udp%3a%2f%2fexodus.desync.com%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.moeking.me"
#       "%3a6969%2fannounce")
