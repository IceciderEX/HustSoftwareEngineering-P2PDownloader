from src.structures.torrent import Torrent
import binascii

torrent_file = Torrent("../../debian-12.1.0-amd64-netinst.iso.torrent")

info_hash = binascii.hexlify(torrent_file.info_hash).decode('utf-8')  # bytes to str
print(info_hash)
print(torrent_file.announce)
print(torrent_file.name)
print(torrent_file.length)
print(torrent_file.piece_length)