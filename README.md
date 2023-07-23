# Clean-Song-AI
This program combines ai vocal remover and automatic speech recognition software into a single CLI python program that removes explicit lyrics from songs.
Install
```
pip install git+https://github.com/JuicetinB/Clean-Song-AI
```
## Google Colab Notebook:
[![Open All Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JuicetinB/Clean-Song-AI/blob/main/Clean.ipynb)
## Dependencies:
[Whisper](https://github.com/openai/whisper) from OpenAI, preferably with some form of CUDA (requires github install and not pip as pip isn't yet updated to support word timestamps
```
pip install git+https://github.com/openai/whisper.git
```
[Demucs](https://github.com/facebookresearch/demucs) from Meta Research
```
pip install -U git+https://github.com/facebookresearch/demucs#egg=demucs
```
For CUDA and gpu support
Check CUDA version with 
```
nvcc --version
```
[PyTorch](https://pytorch.org/get-started/locally/)
You may want to build [from source](https://github.com/pytorch/pytorch#from-source) if on the latest release of CUDA.

Example install for CUDA version 12.1 on Windows:
[CUDA 12.1 download](https://developer.nvidia.com/cuda-12-1-0-download-archive)
```
pip uninstall torch torchvision torchaudio
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121
```
![PyTorch CUDA check](https://github.com/JuicetinB/Clean-Song-AI/blob/main/Screenshot%202023-06-27%20114902.png)

Alternatively, I believe these programs can detect if there's only a cpu in the system

[yt-dlp](https://github.com/yt-dlp) (Optional; required for -l or --link argument)
```
pip install yt-dlp
```
FFmpeg

This program is only tested on windows but might work on other platforms. This is able to run on my personal laptop with 4gb of vram, but you may need to set a smaller whisper model with `-m` if you have less vram

## __main__.py (and sequential.py)
Has the ability to use yt-dlp, Demucs, and Whisper to clean a song given a link, a list of links, a path to a song, or, without any relevant arguments, a fileprompt to select songs. Resulting clean songs are placed in the current directory.
```
py -m cleansong --link "youtube-link"
```
prompts for file selection
```
py -m cleansong --link "https://www.youtube.com/[video]" "https://www.youtube.com/[video]"
```
downloads both of the videos. Also supports links to albums or playlists. Just use quotes because "&" can act wierd in terminals.
```
py -m cleansong --song [song path]
```
uses the song file
```
py -m cleansong --help
```
shows all supported arguments

## Cleaning.py
Intended for use with UVR or similar software that lacks a CLI.
Place three files, one with vocal in the name and one with instrumental in the name, into a folder and provide the path to that folder as an argument.

Currently untested if the command below works
```
py -m cleansong.cleaning --folder [path]
```
