#manually retrieve three files from uvr
#put them in a folder and maybe the folder directory is the argument
#one is a title, one has vocal in the name, one has instrumental in the name; treat them as such
#validate that they are the same length
#run whisper or vosk on the vocal file --small.en
#mute the main file where the transcription matches curse words
#invert these mutes on the instrumental
#merge the files and return output in same folder with _clean
#this will work for individual words but I'm considering adding a window that removes phrases like "blow job"
#list is modified version of https://github.com/web-mech/badwords/blob/master/lib/lang.output
#to get single file input with cli, i could use vr architecture original program: vocal-remover by tsurumeso
#add a command line help
#prereqs: whisper from openai, UVR or equivalent VR software, ffmpeg, pydub, 
#a cool feature would be to compare the words censored to the words that should be censored based on a lyric website to check the accuracy of whisper and warn of any missed words
#if it says neck and the percentage is low, then that's stetchy. and movers?
import whisper
from pydub import AudioSegment
import sys
import os
import argparse
from filter import censor_list

parser = argparse.ArgumentParser(prog='Song cleaning tool', description='Provide a folder with 3 audio files in it resulting from UVR')
parser.add_argument('-f', '--folder','--path', dest='folder', type=str, nargs='*', 
                    help='the path of your folder (default: uses the current directory)', default=[os.getcwd()], action='store')
parser.add_argument('--padding', dest='padding', action='store', nargs=1, default=0.05, type=float,
                    help='the amount of time in seconds added to when whisper detects a word was said (default: .05 seconds)')
parser.add_argument('--format', dest='format', type=str, nargs=1,
                    help='the format of the output ex. wav (default: flac)', default='flac', action='store')
parser.add_argument('-m', '--model', dest='model', type=str,
                    help='the model ex. tiny, tiny.en, base.en, base (default: small.en)', default='small.en', action='store')
args = parser.parse_args()
folder=" ".join(args.folder)
print(f'searching {folder} for 3 audio files')
#print(args.model)
padding=args.padding
audiofiles=[]
music={}
for n in os.listdir(folder):
    if n.lower().endswith(('.wav', '.mp3', '.m4a','.aac','.alac','.flac','.opus','.ogg','.wma','.aif')):
        audiofiles.append(n)
if len(audiofiles)!=3:
    sys.exit("There are not exactly 3 supported audio files in the given folder!")
for name in audiofiles:
    if "vocal" in name.lower():
        music['vocal']=os.path.join(folder,name)
    elif "instrumental" in name.lower():
        music['instrumental']=os.path.join(folder,name)
    else:
        music['original']=os.path.join(folder,name)
model = whisper.load_model(args.model)
output = model.transcribe(music['vocal'], word_timestamps=True,prepend_punctuations="",append_punctuations="")
lyrics = []
print('AI generated lyrics:', output['text'])
for i in output['segments']:
    for j in i['words']:
        lyrics.append(j)
times = []
print(lyrics)
for n in lyrics:
    if n['word'].lower().strip() in censor_list:
        print(f'removing the word {n["word"]} from {n["start"]} to {n["end"]} seconds')
        if (n["start"]-padding)*1000 <= 0:
            times.append([0,int((n["end"]+padding)*1000)])
        else:
            times.append([int((n["start"]-padding)*1000),int((n["end"]+padding)*1000)])
mainaudio = AudioSegment.from_file(music['original'])
instaudio = AudioSegment.from_file(music['instrumental'])
clean = mainaudio
for n in times:
    start=n[0]
    end=n[1]
    background=instaudio[start:end]
    clean=clean[:start]+background+clean[end:]

clean.export(((music['original']).rsplit('.', 1))[0]+f' clean.{args.format}',format=args.format)