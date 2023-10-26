# @auther 李鑫煜

import os
import requests
import subprocess
import concurrent.futures
import time
import logging
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)



# Function to download the M3U8 file
def download_m3u8(url):
    """
    发送下载请求
    :param url: 请求URL
    :return:
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch M3U8 playlist. Status code: {response.status_code}")


# Function to parse the M3U8 playlist and extract segment URLs
def parse_m3u8(m3u8_content):
    """
    解析m3u8得到TS文件列表
    :param m3u8_content: m3u8内容
    :return:
    """
    lines = m3u8_content.split('\n')
    segment_urls = [urljoin(m3u8_url, line.strip()) for line in lines if line and not line.startswith("#")]
    return segment_urls


def download_segment(segment_url, output_dir, index):
    """
    下载单个TS文件
    :param segment_url:  TS文件的请求列表
    :param output_dir: TS输出位置
    :param index: 序号
    :return:
    """
    try:
        response = requests.get(segment_url, stream=True)
        if response.status_code == 200:
            segment_filename = os.path.join(output_dir, f"segment_{index:04d}.ts")
            with open(segment_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                logging.info(f"Downloaded segment_{index:04d}.ts")
        else:
            logging.error(f"Failed to download segment_{index:04d}.ts")
    except Exception as e:
        logging.error(f"An error occurred while downloading segment_{index:04d}.ts: {str(e)}")


# Function to download all segments
def download_segments(segment_urls, output_dir, start_time=None):
    """
    下载TS文件
    :param segment_urls: TS文件的请求列表
    :param output_dir: TS输出位置
    :return:
    """
    os.makedirs(output_dir, exist_ok=True)
    total_segments = len(segment_urls)
    downloaded_segments = 0
    total_bytes = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(download_segment, url, output_dir, i): url for i, url in enumerate(segment_urls)}
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                future.result()
                downloaded_segments += 1
                segment_size = os.path.getsize(os.path.join(output_dir, f"segment_{downloaded_segments - 1:04d}.ts"))
                total_bytes += segment_size

                # Calculate progress and speed
                progress = downloaded_segments / total_segments * 100
                average_speed = total_bytes / (1024 * (time.time() - start_time))  # Average speed in KB/s

                logging.info(
                    f"Downloaded {downloaded_segments}/{total_segments} segments - {progress:.2f}% complete ({average_speed:.2f} KB/s)")

            except Exception as e:
                logging.error(f"Downloading of {url} generated an exception: {str(e)}")


# Function to merge segments
def merge_segments(output_dir, output_filename):
    """
    合并TS文件
    :param output_dir: 输出位置
    :param output_filename: 输出文件名
    :return:
    """
    ts_files = [os.path.join(output_dir, filename) for filename in os.listdir(output_dir) if filename.endswith(".ts")]
    try:
        cmd = ['ffmpeg', '-i', 'concat:' + '|'.join(ts_files), '-c', 'copy', output_filename]
        subprocess.run(cmd, check=True)
        logging.info(f'Successfully merged {len(ts_files)} .ts files into {output_filename}')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error merging files: {e}')
    except Exception as e:
        logging.error(f'An error occurred: {e}')
    clean_up(ts_files)
    logging.info(".ts files were cleaned up!")
    logging.info(f"Video saved as {output_filename}")


def clean_up(self):
    """
    删除TS文件
    :return: 无
    """
    try:
        for ts_file in self.ts_files:
            os.remove(ts_file)
            logging.info(f'Deleted {ts_file}')
    except Exception as e:
        logging.error(f'An error occurred while cleaning up files: {e}')



def jiekou(m3u8_:str, output_:str, filen:str):
    """
    接口
    :param m3u8_: m3u8url
    :param output_: 输出位置
    :param filen: 文件名
    :return:
    """
    m3u8_url = m3u8_
    output_dir = output_
    filename = filen
    output_filename = output_dir + "\\" + filename

    try:
        m3u8_content = requests.get(m3u8_url).text
        segment_urls = [urljoin(m3u8_url, line.strip()) for line in m3u8_content.split('\n') if
                        line and not line.startswith("#")]
        start_time = time.time()
        download_segments(segment_urls, output_dir)
        merge_segments(output_dir, output_filename)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
