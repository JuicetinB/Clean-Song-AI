import yt_dlp
import os

def download(URLS):
    downloadfiles=[]
    def filename(d):
        if d['status'] == 'finished':
            downloadfiles.append(os.getcwd()+'\\'+d['filename'])
    downloadfiles=[]
    with yt_dlp.YoutubeDL({'format':'m4a', 'progress_hooks':[filename]}) as ydl:
        ydl.download(URLS)
    return downloadfiles