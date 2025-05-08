from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import subprocess


def scrape_youtube(query):

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(f"https://www.youtube.com/results?search_query={query}")

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    url_list = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if '/watch?v=' in href:
            url_list.append(f"https://www.youtube.com{href}")

    driver.quit()
    return url_list



def dl_and_convert(url):

    yt_dlp_command = [
        'yt-dlp',
        '-x',
        '--audio-format','mp3',
        '--audio-quality','0',
        '--quiet',
        '-o','downloads/video-audio.mp3',
        '--force-overwrites',
        url
    ]

    try:
        subprocess.run(yt_dlp_command,check=True)
        print("Download completed successfully")
        return 'downloads/video-audio.mp3'
    except subprocess.CalledProcessError as e:
        print(f'Download failed with return code {e.returncode}')
        return ''



