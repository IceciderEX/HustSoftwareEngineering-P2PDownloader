import asyncio
import logging
import signal
from asyncio import CancelledError

from src.torrent.client import TorrentClient
from src.torrent.torrent import Torrent


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s',
                        datefmt='%Y/%m/%d %I:%M:%S %p')
    loop = asyncio.get_event_loop()
    client = TorrentClient(Torrent("file/"))
    task = loop.create_task(client.start())
    task2 = loop.create_task(client.return_download_time())

    def signal_handler(*_):
        logging.info('Exiting, please wait until everything is shutdown...')
        client.stop()
        task.cancel()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        loop.run_until_complete(task)
        loop.run_until_complete(task2)
    except CancelledError:
        logging.warning('Event loop was canceled')


if __name__ == '__main__':
    main()
