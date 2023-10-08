import asyncio
import logging
import signal
from asyncio import CancelledError

from src.torrent.client import TorrentClient
from src.torrent.torrent import Torrent


def main():
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    client = TorrentClient(Torrent("../file/1.torrent"))
    task = loop.create_task(client.start())

    def signal_handler(*_):
        logging.info('Exiting, please wait until everything is shutdown...')
        client.stop()
        task.cancel()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        loop.run_until_complete(task)
    except CancelledError:
        logging.warning('Event loop was canceled')


if __name__ == '__main__':
    main()
