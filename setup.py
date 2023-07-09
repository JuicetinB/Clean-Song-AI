from setuptools import setup

setup(
   name='Clean-Song-AI',
   version='1.0',
   description='Exports clean versions of songs',
   author='JuicetinB',
   author_email='jabuonato@gmail.com'
   packages=['Clean-Song-AI'],
   install_requires=['demucs', 'whisper', 'pydub'], #external packages as dependencies
)