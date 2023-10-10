import requests
import logging
from urllib.parse import unquote
from src.magnetlink.MagnetlinkParser import magnetlinkParser


def get_torrent(url):
    response = requests.get(url)
    if response.status_code == 200:
        output_file = response.headers['Torrent-Name'] + '.torrent'
        decoded_text = unquote(output_file)
        with open(decoded_text, "wb") as f:
            f.write(response.content)
        print("Torrent file saved to", decoded_text)
    elif response.status_code == 504:
        print("Overtime, Maybe this magnetlink cannot convert to torrent")
    else:
        print("Failed to retrieve the torrent file. HTTP status code:", response.status_code)


def magnet2torrent(magnetlink):
    parsed_link = magnetlinkParser(magnetlink=magnetlink).parse_magnetlink()
    url = "https://m2t.lolicon.app/m/" + parsed_link.info_hash
    get_torrent(url)


magnet2torrent("magnet:?xt=urn:btih:08ebb0b0f0ef32367d7d07e35ce71c361426e506")  # 狂飙22集

