import yt_dlp
import os
import requests
from bs4 import BeautifulSoup as BS

def download(URLS):
    downloadfiles=[]
    def filename(d):
        if d['status'] == 'finished':
            downloadfiles.append(os.getcwd() + '\\' + d['filename'])
    downloadfiles=[]
    with yt_dlp.YoutubeDL({'format':'m4a', 'progress_hooks':[filename]}) as ydl:
        ydl.download(URLS)
    return downloadfiles

def get_lyrics(link):
    req=requests.get(link, headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'})
    print(req.content)
    content=BS(req.content, 'html.parser')
    #print(content)
    #lyrics=content.select('.non-expandable description style-scope ytmusic-description-shelf-renderer')
    #print(lyrics)
    #print(lyrics.get_text())

    #method 1: use class from music page and scrape
    #method 2: use musixmatch api and title search, then have user confirm song title and artist. CAN ONLY GET 30% OF LYRICS PER SONG WITHOUT PAYING
    #track.subtitle.get gives LRC file with times for lines
    #track.lyrics.get gives normal lyric text; f_has_lyrics
    #track.richsync.get has individual character timing; f_has_rich_sync=1
    #print('hello')

#example api usage
#import requests

#response = requests.get("link" + 'variable')
#print(response.json())

#https://huggingface.co/spaces/akhaliq/demucs has an api that I can use to make this a web app or use colabs
#I could make my own space, but I need to check demucs -d cpu performance
#https://mvsep.com/ is a good site

#get_lyrics("https://music.youtube.com/watch?v=ir98TwbImtQ&feature=share")