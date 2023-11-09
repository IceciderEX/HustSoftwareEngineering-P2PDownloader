import logging
import re
import asyncio


class magnetLink:
    """
    magnetlink封装类，保存info_hash，display_name，trackers
    """
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
    """
    解析磁力链接，保存为magnetlink实例
    """
    magnetlink = ""

    def __init__(self, magnetlink):
        self.magnetlink = magnetlink

    def parse_magnetlink(self):
        info_hash = ""
        display_name = ""
        trackers = []

        # TODO
        # magnetlink对应的正则表达式
        pattern = 

        # TODO
        # 对正则表达式获得的group进行处理

        return magnetLink(link=self.magnetlink, info_hash=info_hash, display_name=display_name, trackers=trackers)