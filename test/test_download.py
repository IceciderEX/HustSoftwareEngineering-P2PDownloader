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
    client = TorrentClient(Torrent("file/debian-9.3.0-amd64-netinst.torrent"))
    task = loop.create_task(client.start())

    def signal_cancel(ctrl_type):
        logging.info('Exiting, please wait until everything is shutdown...')
        client.stop()
        task.cancel()

    # def signal_pause(*_):
    #     global paused
    #     if not paused:
    #         paused = True
    #         logging.info('Pausing download')
    #         client.pause()
    #     else:
    #         paused = False
    #         logging.info('Pausing download')
    #         client.restart()
    # client.pause()
    # client.restart()
    # loop.call_at(future_time,client.pause())
    signal.signal(signal.SIGINT, signal_cancel)
    # signal.signal(signal.SIGTSTP, signal_pause)
    try:
        loop.run_until_complete(task)

    except CancelledError:
        logging.warning('Event loop was canceled')


if __name__ == '__main__':
    main()
