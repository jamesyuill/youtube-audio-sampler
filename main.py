from threading import Thread
from download import scrape_youtube, dl_and_convert
from cut_up import cut_up_audio


def scrape_web(query):
    url_list = scrape_youtube(query)
    audio_path = dl_and_convert(url_list[video_num])
    cut_up_audio(audio_path)


def start_scraping(query):
    print('scraping...')
    Thread(target=scrape_web(query)).start()

query = input('give me a word: ')
video_num = int(input('give me a number between 1-10: '))

start_scraping(query)