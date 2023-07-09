from setuptools import setup

setup(
   name='cleansong',
   version='1.0',
   description='Exports clean versions of songs',
   author='JuicetinB',
   packages=['cleansong'],
   install_requires=['demucs', 'whisper', 'pydub'], #external packages as dependencies
)