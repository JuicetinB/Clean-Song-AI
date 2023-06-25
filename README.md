# Clean-Song-AI
This program combines ai vocal remover and automatic speech recognition software into a single CLI python program that removes explicit lyrics from songs.
## Prerequisites:
[Whisper](https://github.com/openai/whisper) from OpenAI, preferably with some form of CUDA (requires github install and not pip as pip isn't yet updated to support word timestamps
```
pip install git+https://github.com/openai/whisper.git
```
[Demucs](https://github.com/facebookresearch/demucs) from Meta Research
```
pip install -U demucs
```
[yt-dlp](https://github.com/yt-dlp) (Optional; required for -l or --link argument)
```
pip install yt-dlp
```
FFmpeg

This program is only tested on windows but might work on other platforms. This is able to run on my personal laptop with 4gb of vram, but you may need to set a smaller whisper model with `-m` if you have less vram

## Main.py
Has the ability to use yt-dlp, Demucs, and Whisper to clean a song given a link, a list of links, a path to a song, or, without any relevant arguments, a fileprompt to select songs. Resulting clean songs are placed in the current directory.
```
py [path]/main.py
```
prompts for file selection
```
py [path]/main.py --link "https://www.youtube.com/[video]"
```
downloads the video. Also supports multiple links or links to albums or playlists. Just use quotes because "&" can act wierd in terminals.
```
py [path]/main.py --song [song path]
```
uses the song file
```
py [path]/main.py --help
```
shows all supported arguments

## Cleaning.py
Intended for use with UVR or similar software that lacks a CLI.
Place three files, one with vocal in the name and one with instrumental in the name, into a folder.
```
py [path]/cleaning.py --folder [path]
```
