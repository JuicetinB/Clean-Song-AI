from setuptools import setup, find_packages

setup(
   name='cleansong',
   version='1.0',
   description='Exports clean versions of songs',
   author='JuicetinB',
   author_email='jabuonato@gmail.com',
   packages=['cleansong'],
   install_requires=[
       'demucs @ git+https://github.com/facebookresearch/demucs#egg=demucs',
       'whisper @ git+https://github.com/openai/whisper.git',
       'torch'
   ], #external packages as dependencies 'demucs', 'whisper', 'pydub'
)