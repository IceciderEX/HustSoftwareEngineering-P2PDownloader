import os
import requests
import subprocess
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Define the M3U8 URL you want to download
m3u8_url = "https://videotx-platform.cdn.huya.com/leaf/1048585/1199566795719/61787241/15469627_ebd0887ed7bb099558833e816768d860_264_720_6_ai.m3u8"

# Define the output directory and filename for the final video
output_dir = "D:/University/early_3rd/m3u8download"
output_filename = "D:/University/early_3rd/m3u8download/czh.mp4"


# Function to download the M3U8 file
def download_m3u8(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch M3U8 playlist. Status code: {response.status_code}")


# Function to parse the M3U8 playlist and extract segment URLs
def parse_m3u8(m3u8_content):
    lines = m3u8_content.split('\n')
    segment_urls = [urljoin(m3u8_url, line.strip()) for line in lines if line and not line.startswith("#")]
    return segment_urls


# Function to download M3U8 segments and save them to the output directory
def download_segments(segment_urls, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for i, segment_url in enumerate(segment_urls):
        response = requests.get(segment_url)
        if response.status_code == 200:
            segment_filename = os.path.join(output_dir, f"segment_{i}.ts")
            with open(segment_filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded segment {i}")
        else:
            print(f"Failed to download segment {i}")


# Function to merge downloaded segments into a single video file using FFmpeg
def merge_segments(output_dir, output_filename):
    input_pattern = os.path.join(output_dir, "segment_*.ts")
    subprocess.run([
        "ffmpeg",
        "-i", input_pattern,
        "-c", "copy",
        output_filename
    ])
    print(f"Video saved as {output_filename}")


if __name__ == "__main__":
    try:
        m3u8_content = download_m3u8(m3u8_url)
        segment_urls = parse_m3u8(m3u8_content)
        download_segments(segment_urls, output_dir)
        merge_segments(output_dir, output_filename)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
