import asyncio
from src.torrent.tracker import Tracker
from src.torrent.torrent import Torrent


async def test_connect():
    filepath = 'file/debian-12.1.0-amd64-netinst.iso.torrent'
    torrent_file = Torrent(filepath)
    bt_tracker = Tracker(torrent_file)
    resp = await bt_tracker.connect(True)
    assert resp.peers is not None
    await bt_tracker.close()


if __name__ == '__main__':
    asyncio.run(test_connect())
