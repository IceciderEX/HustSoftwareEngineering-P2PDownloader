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
        pattern = r"magnet:\?xt=urn:btih:(\w+)&dn=([^&]+)&tr=([^&]+(?:&tr=[^&]+)*)"

        match = re.match(pattern, self.magnetlink)
        if match:
            info_hash = match.group(1)
            display_name = match.group(2)
            trackers = match.group(3).split("&tr=")

        return magnetLink(link=magnetLink, info_hash=info_hash, display_name=display_name, trackers=trackers)


link_to_parse = magnetlinkParser(
    "magnet:?xt=urn:btih:4225824a42f4afceec51cf73ae85fdc76f14aebd&dn=Mind.Games.rar&tr=udp%3a%2f%2ftracker.torrent.eu"
    ".org%3a451%2fannounce&tr=udp%3a%2f%2fexodus.desync.com%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.moeking.me"
    "%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce&tr=udp%3a%2f%2fopen.stealth.si%3a80"
    "%2fannounce&tr=udp%3a%2f%2ftracker.theoks.net%3a6969%2fannounce&tr=udp%3a%2f%2fmovies.zsw.ca%3a6969%2fannounce"
    "&tr=udp%3a%2f%2ftracker.tiny-vps.com%3a6969%2fannounce&tr=udp%3a%2f%2ftracker-udp.gbitt.info%3a80%2fannounce&tr"
    "=http%3a%2f%2ftracker.gbitt.info%3a80%2fannounce&tr=https%3a%2f%2ftracker.gbitt.info%3a443%2fannounce&tr=http%3a"
    "%2f%2ftracker.ccp.ovh%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.ccp.ovh%3a6969%2fannounce&tr=udp%3a%2f%2ftracker"
    ".dler.com%3a6969%2fannounce&tr=http%3a%2f%2ftracker.bt4g.com%3a2095%2fannounce&tr=udp%3a%2f%2fopen.demonii.com"
    "%3a1337%2fannounce&tr=udp%3a%2f%2fexplodie.org%3a6969%2fannounce&tr=udp%3a%2f%2fp4p.arenabg.com%3a1337"
    "%2fannounce&tr=udp%3a%2f%2ftracker.dler.org%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.openbittorrent.com%3a6969"
    "%2fannounce&tr=udp%3a%2f%2fuploads.gamecoast.net%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.cyberia.is%3a6969"
    "%2fannounce&tr=udp%3a%2f%2fipv4.tracker.harry.lu%3a80%2fannounce&tr=udp%3a%2f%2fipv6.tracker.harry.lu%3a80"
    "%2fannounce&tr=udp%3a%2f%2ftracker1.bt.moack.co.kr%3a80%2fannounce&tr=udp%3a%2f%2fopentracker.i2p.rocks%3a6969"
    "%2fannounce&tr=udp%3a%2f%2feddie4.nl%3a6969%2fannounce&tr=udp%3a%2f%2fbt1.archive.org%3a6969%2fannounce&tr=udp"
    "%3a%2f%2ftracker.swateam.org.uk%3a2710%2fannounce&tr=http%3a%2f%2ftracker.openbittorrent.com%3a80%2fannounce&tr"
    "=http%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce&tr=https%3a%2f%2ftracker1.520.jp%3a443%2fannounce&tr"
    "=https%3a%2f%2ftracker.tamersunion.org%3a443%2fannounce&tr=https%3a%2f%2ftracker.imgoingto.icu%3a443%2fannounce"
    "&tr=http%3a%2f%2fnyaa.tracker.wf%3a7777%2fannounce&tr=udp%3a%2f%2ftracker2.dler.org%3a80%2fannounce&tr=udp%3a%2f"
    "%2ftracker.dump.cl%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.bittor.pw%3a1337%2fannounce&tr=udp%3a%2f%2ftracker.4"
    ".babico.name.tr%3a3131%2fannounce&tr=udp%3a%2f%2fsanincode.com%3a6969%2fannounce&tr=udp%3a%2f%2fretracker01-msk"
    "-virt.corbina.net%3a80%2fannounce&tr=udp%3a%2f%2fprivate.anonseed.com%3a6969%2fannounce&tr=udp%3a%2f%2fopen.free"
    "-tracker.ga%3a6969%2fannounce&tr=udp%3a%2f%2fisk.richardsw.club%3a6969%2fannounce&tr=udp%3a%2f%2fhtz3.noho.st"
    "%3a6969%2fannounce&tr=udp%3a%2f%2fepider.me%3a6969%2fannounce&tr=udp%3a%2f%2fbt.ktrackers.com%3a6666%2fannounce"
    "&tr=udp%3a%2f%2facxx.de%3a6969%2fannounce&tr=udp%3a%2f%2faarsen.me%3a6969%2fannounce&tr=udp%3a%2f"
    "%2f6ahddutb1ucc3cp.ru%3a6969%2fannounce&tr=udp%3a%2f%2fyahor.of.by%3a6969%2fannounce&tr=udp%3a%2f%2fv2.iperson"
    ".xyz%3a6969%2fannounce&tr=udp%3a%2f%2ftracker1.myporn.club%3a9337%2fannounce&tr=udp%3a%2f%2ftracker.therarbg.com"
    "%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.qu.ax%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.publictracker.xyz"
    "%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.netmap.top%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.farted.net%3a6969"
    "%2fannounce&tr=udp%3a%2f%2ftracker.cubonegro.lol%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.0x7c0.com%3a6969"
    "%2fannounce&tr=udp%3a%2f%2fthouvenin.cloud%3a6969%2fannounce&tr=udp%3a%2f%2fthinking.duckdns.org%3a6969"
    "%2fannounce&tr=udp%3a%2f%2ftamas3.ynh.fr%3a6969%2fannounce&tr=udp%3a%2f%2fryjer.com%3a6969%2fannounce&tr=udp%3a"
    "%2f%2frun.publictracker.xyz%3a6969%2fannounce&tr=udp%3a%2f%2frun-2.publictracker.xyz%3a6969%2fannounce&tr=udp%3a"
    "%2f%2fpublic.tracker.vraphim.com%3a6969%2fannounce&tr=udp%3a%2f%2fpublic.publictracker.xyz%3a6969%2fannounce&tr"
    "=udp%3a%2f%2fpublic-tracker.cf%3a6969%2fannounce&tr=udp%3a%2f%2fopentracker.io%3a6969%2fannounce&tr=udp%3a%2f"
    "%2fopen.u-p.pw%3a6969%2fannounce&tr=udp%3a%2f%2fopen.dstud.io%3a6969%2fannounce&tr=udp%3a%2f%2foh.fuuuuuck.com"
    "%3a6969%2fannounce&tr=udp%3a%2f%2fnew-line.net%3a6969%2fannounce&tr=udp%3a%2f%2fmoonburrow.club%3a6969"
    "%2fannounce&tr=udp%3a%2f%2fmail.segso.net%3a6969%2fannounce&tr=udp%3a%2f%2ffree.publictracker.xyz%3a6969"
    "%2fannounce&tr=udp%3a%2f%2fcarr.codes%3a6969%2fannounce&tr=udp%3a%2f%2fbt2.archive.org%3a6969%2fannounce&tr=udp"
    "%3a%2f%2f6.pocketnet.app%3a6969%2fannounce&tr=udp%3a%2f%2f1c.premierzal.ru%3a6969%2fannounce&tr=udp%3a%2f"
    "%2ftracker.t-rb.org%3a6969%2fannounce&tr=udp%3a%2f%2ftracker.srv00.com%3a6969%2fannounce&tr=udp%3a%2f%2ftracker"
    ".artixlinux.org%3a6969%2fannounce&tr=udp%3a%2f%2ftorrents.artixlinux.org%3a6969%2fannounce&tr=udp%3a%2f%2fpsyco"
    ".fr%3a6969%2fannounce&tr=udp%3a%2f%2fmail.artixlinux.org%3a6969%2fannounce&tr=udp%3a%2f%2flloria.fr%3a6969"
    "%2fannounce&tr=udp%3a%2f%2ffh2.cmp-gaming.com%3a6969%2fannounce&tr=udp%3a%2f%2fconcen.org%3a6969%2fannounce&tr"
    "=udp%3a%2f%2fboysbitte.be%3a6969%2fannounce&tr=udp%3a%2f%2faegir.sexy%3a6969%2fannounce").parse_magnetlink()

print(link_to_parse.info_hash)
print(link_to_parse.trackers)
print(link_to_parse.display_name)