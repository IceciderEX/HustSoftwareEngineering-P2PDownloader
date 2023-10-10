#@auther 李鑫煜
import os
import requests
import subprocess
from urllib.parse import urljoin

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
            segment_filename = os.path.join(output_dir, f"segment_%04d.ts" % i)
            with open(segment_filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded segment_%04d.ts" % i)
        else:
            print(f"Failed to download segment_%04d.ts" % i)


# Function to merge downloaded segments into a single video file using FFmpeg
def merge_segments(output_dir, output_filename):
    ts_files = []
    for filename in os.listdir(output_dir):
        if filename.endswith(".ts"):
            ts_files.append(os.path.join(output_dir, filename))
    try:
        # 构建ffmpeg命令，将多个.ts文件合并成一个.mp4文件
        cmd = ['ffmpeg', '-i', 'concat:' + '|'.join(ts_files), '-c', "copy", output_filename]

        # 运行ffmpeg命令
        subprocess.run(cmd, check=True)
        print(f'Successfully merged {len(ts_files)} .ts files into {output_filename}')
    except subprocess.CalledProcessError as e:
        print(f'Error merging files: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')
    clean_up(ts_files)
    print(".ts files were cleaned up!")
    print(f"Video saved as {output_filename}")

def clean_up(ts_files):
    try:
        for ts_file in ts_files:
            os.remove(ts_file)
            print(f'Deleted {ts_file}')
    except subprocess.CalledProcessError as e:
        print(f'Error merging files: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')
if __name__ == "__main__":
    # Define the M3U8 URL you want to download
    m3u8_url = input("input the M3U8 URL you want to download: ")

    # Define the output directory and filename for the final video
    output_dir = input("input the directory for the video to download: ") #如D:\University\early_3rd\m3u8download
    output_filename = input("input the filename for the video you want to download: ") #如D:\University\early_3rd\m3u8download\video.mp4
    try:
        m3u8_content = download_m3u8(m3u8_url)
        segment_urls = parse_m3u8(m3u8_content)
        download_segments(segment_urls, output_dir)
        merge_segments(output_dir, output_filename)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
