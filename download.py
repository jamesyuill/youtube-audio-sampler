from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import subprocess


def scrape_youtube(query):

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(f"https://www.youtube.com/results?search_query={query}")

    time.sleep(3)

    try:
        dialogue = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "dialog"))
        )
        dialogue.click()
        dialogue.send_keys(Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.ENTER)
        print('cookie clicked')
    except:
        print("Cookie modal not found or already dismissed.")


    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    shorts = soup.find_all('a',id="thumbnail")

    url_list = []

    
    # for a_tag in shorts:
    #     print(a_tag)
    #     if 'href' in a_tag.attrs:
    #         href = a_tag['href']
    #         # img_src  =a_tag['src']
    #         url = f"https://www.youtube.com{href}"
    #         url_list.append(url)

    for a_tag in shorts:
        if 'href' in a_tag.attrs:
            href = a_tag['href']
            if '/shorts/' in href:
                url = f"https://www.youtube.com{href}"
                url_list.append(url)



            #watch?v=
        # if '/shorts/' in href and img_tag and 'src' in img_tag.attrs:
        #     img_src  =img_tag['src']
        #     url = f"https://www.youtube.com{href}"
        #     url_list.append({'img_src':img_src, 'url':url})


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



