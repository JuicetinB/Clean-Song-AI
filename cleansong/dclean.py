import whisper
from pydub import AudioSegment, silence
import sys
import os
from cleansong.filter import censor_list
import torch
import gc

def identify(vocal,model="small.en",padding=.05):
    model = whisper.load_model(model)
    times = identifynomodel(model,vocal,padding)
    del(model)
    torch.cuda.empty_cache()
    gc.collect()
    return times


def identifynomodel(model, vocal, padding=.05):
    output = model.transcribe(vocal, word_timestamps=True, prepend_punctuations="", append_punctuations="", no_speech_threshold=.6,)
    lyrics = []
    print('AI generated lyrics:', output['text'])
    for i in output['segments']:
        for j in i['words']:
            lyrics.append(j)
    times = []
    #print(lyrics)
    for n in lyrics:
        if n['word'].lower().strip() in censor_list:
            print(f'removing the word {n["word"]} from {n["start"]} to {n["end"]} seconds')
            #prevent negative times for words at the start of songs
            if (n["start"]-padding)*1000 <= 0:
                times.append([0,int((n["end"]+padding)*1000)])
            else:
                times.append([int((n["start"]-padding)*1000),int((n["end"]+padding)*1000)])
    return times

def clean(full,novocal,times,_format):
    mainaudio = AudioSegment.from_file(full)
    backing = AudioSegment.from_file(novocal)
    clean = mainaudio
    for n in times:
        start=n[0]
        end=n[1]
        censored=backing[start:end]
        clean=clean[:start]+censored+clean[end:]
        clean.export((full.rsplit('.', 1))[0]+f' clean.{_format}',format=_format)
    return None

def remove_silence(vocal, padding=50):
    raw = AudioSegment.from_file(vocal)
    #makes list of start and end times; st for silent times
    st = silence.detect_silence(raw, min_silence_len=2000, silence_thresh=-35)
    #adds length; total silent time; adjusted time in output file
    i=0
    totals=0
    gap = AudioSegment.silent(duration=padding)
    while i<len(st):
        length=st[i][1]-st[i][0]-padding
        #st[i][2] is the length of the silent that gets cut from this segment
        st[i].append(length)
        #time of cut in output audio file
        ostart=st[i][0]-totals
        st[i].append(ostart)
        #takes out a silent segment while totals accounts for previous segments taken out; st[i][1]-totals is the same as st[i][3]+length
        raw = raw[:ostart]+ gap + raw[st[i][1]-totals:]
        totals+=length
        i+=1
    #find some way to offset whisper output times by all the silent sections before them
    #make a list of the times in the output vocal file with silence cut out; if whisperstarttime>x, add sum of all silent sections before time to time
    raw.export(vocal, format = 'wav')
    return st

def timeadjust(times : list, st : list):
    for segments in times:
        for silence in st:
            if segments[1]>=silence[0]:
                segments[0]+=silence[2]
                segments[1]+=silence[2]
            else:
                break
    return times
#idea: use the lyrics as the initial prompt; update: didn't improve