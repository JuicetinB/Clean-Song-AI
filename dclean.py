import whisper
from pydub import AudioSegment
import sys
import os
from filter import censor_list

def identify(vocal,model="small.en",padding=.05):
    model = whisper.load_model(model)
    output = model.transcribe(vocal, word_timestamps=True,prepend_punctuations="",append_punctuations="")
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