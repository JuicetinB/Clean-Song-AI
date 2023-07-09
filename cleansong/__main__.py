import argparse
from cleansong import dlp, dclean, dsep
import tkinter as tk
from tkinter import filedialog
import whisper
import gc
import torch
import multiprocessing

def cleansongmemory(songs):
    print("creating all splits first")
    #4 variables to store in lists: novocals, vocals, st, times
    novocals, vocals, sts, times = [], [], [], []
    count = range(len(songs))
    print("separating all songs")
    for i in count:
        novocal , vocal = dsep.vocals(songs[i])
        novocals.append(novocal)
        vocals.append(vocal)
    torch.cuda.empty_cache()
    gc.collect()
    #this one could be multithreaded somehow
    print("removing silence from all vocal splits")
    #for i in count:
        #st = dclean.remove_silence(vocals[i], (args.padding*1000))
        #sts.append(st)
    silence_args=[]
    for vocal in vocals:
        silence_args.append((vocal, (args.padding*1000)))
    with multiprocessing.Pool(processes=8) as p1:
        sts=p1.starmap(dclean.remove_silence, silence_args)
    print("running Whisper text-to-speech")
    #globally load model
    model = whisper.load_model(args.model)
    for i in count:
        time = dclean.identifynomodel(model, vocals[i], args.padding)
        times.append(time)
    #globally delete model
    model.cpu()
    del model
    torch.cuda.empty_cache()
    gc.collect()
    print("removing swear words from all songs")
    #this one could be multithreaded somehow and split up
    for i in count:
        times[i] = dclean.timeadjust(times[i],sts[i])
    items=[]
    i=0
    while i<len(songs):
        items.append((songs[i], novocals[i], times[i], args.format))
        i+=1
    pool2=multiprocessing.Pool(processes=8)
    out=pool2.starmap_async(dclean.clean, items)
    out.wait()
    #load demucs globally? not sure if possible

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Song cleaning tool', description='Provide a song and most swear words will be censored')
    parser.add_argument('-s', '--song','--path', dest='song', type=str, 
                        help='The path of your song. Make sure that either no spaces are in the path or that you put quotation marks around each path (default: prompts for file select or uses youtube links)', default=None, action='store')
    parser.add_argument('-l', '--link','--links', dest='links', type=str, nargs='*', 
                        help='Provide youtube links instead of files using yt-dlp. Please use quotes around each link or do not include "&"', default=None, action='store')
    #parser.add_argument('--split', dest='s_out', action='store', type=str,
    #                    help='the output folder for the split files (default: same as input song path)')
    parser.add_argument('--padding', dest='padding', action='store', default=0.05, type=float,
                        help='the amount of time in seconds added to when whisper detects a word was said (default: .05 seconds)')
    parser.add_argument('--format', dest='format', type=str, nargs=1,
                        help='the format of the clean output ex. wav , mp3 (default: flac)', default='flac', action='store')
    parser.add_argument('-m', '--model', dest='model', type=str,
                        help='the whisper model ex. tiny, tiny.en, base.en, base (default: small.en)', default='small.en', action='store')
    #parser.add_argument('-o', '--out', '--output', dest='out', type=str,
    #                    help='the folder where the clean song is saved to (default: same directory as input song)', default=None, action='store')
    args = parser.parse_args()
    #all arguments
    if args.song == None and args.links == None:
        root = tk.Tk()
        root.withdraw()
        songs = filedialog.askopenfilenames(title="choose song files", filetypes=[("Audio Files",'.wav .mp3 .m4a .aac .alac .flac .opus .ogg .wma .aif')])
    elif args.song == None:
        songs = dlp.download(args.links)
    else:
        songs = [args.song]
        songs = songs + dlp.download(args.links)
    
    cleansongmemory(songs)