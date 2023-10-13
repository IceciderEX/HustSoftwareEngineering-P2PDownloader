import requests
from bs4 import BeautifulSoup
import os


def capture(url, path):
    """
    自动检测获取网页的mp4和mp3文件
    :param url: 要获取的网页url
    :param path: 要下载到的位置
    :return: TRUE or FALSE
    """
    # 步骤1：发送 HTTP 请求
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        page_content = response.text
    else:
        return False

    # 步骤2：解析页面内容
    soup = BeautifulSoup(page_content, 'html.parser')

    # 查找视频和音频链接
    video_links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('.mp4')]
    audio_links = [source['src'] for source in soup.find_all('source', src=True) if source['src'].endswith('.mp3')]

    # 步骤3：下载视频和音频
    for video_link in video_links:
        video_response = requests.get(url + video_link, headers=headers)
        with open(os.path.join(path, 'video.mp4'), 'wb') as f:
            f.write(video_response.content)

    for audio_link in audio_links:
        audio_response = requests.get(url + audio_link, headers=headers)
        with open(os.path.join(path, 'audio.mp3'), 'wb') as f:
            f.write(audio_response.content)
    return True


