from setuptools import setup, find_packages

setup(
   name='cleansong',
   version='1.0',
   description='Exports clean versions of songs',
   author='JuicetinB',
   author_email='jabuonato@gmail.com'
   packages=find_packages(),
   install_requires=[], #external packages as dependencies 'demucs', 'whisper', 'pydub'
)