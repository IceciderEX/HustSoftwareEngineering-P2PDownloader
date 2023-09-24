import re


class magnetLink:

    def __init__(self, link, info_hash, display_name, trackers):
        self.link = link
        self.info_hash = info_hash
        self.display_name = display_name
        self.trackers = trackers


class magnetlinkParser:
    magnetlink = ""

    def __init__(self, magnetlink):
        self.magnetlink = magnetlink

    def parse_magnetlink(self):
        info_hash = ""
        display_name = ""
        trackers = []
        pattern = r"magnet:\?xt=urn:btih:(\w+)&dn=([^&]+)&tr=([^&]+)"

        match = re.match(pattern, self.magnetlink)
        if match:
            info_hash = match.group(1)
            display_name = match.group(2)
            trackers = match.group(3).split(",")

        return magnetLink(link=magnetLink, info_hash=info_hash, display_name=display_name, trackers=trackers)


link_to_parse = magnetlinkParser(
    "magnet:?xt=urn:btih:20CF64B3DEDD1A4DF47B3D03616BAC667D9BCC72&dn=example_file&tr=http%3A%2F"
    "%2Ftracker.example.com%3A6969%2Fannounce").parse_magnetlink()

print("infoHash:", link_to_parse.info_hash)
print("displayName:", link_to_parse.display_name)
print("trackers:", link_to_parse.trackers)
