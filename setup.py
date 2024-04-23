#! /usr/bin/env python

from distutils.core import setup

setup(name='GZDoomRun',
      version='1.4.0-1',
      description='A small linux program for loading GZDoom mods a little easier. ',
      long_description="""
This a persosnal program that was originally just a simple python sciript meant to used with Steam to help me load doom mods easier, but has evolved into a full blown Doom Loader that has a few command line options that make it a fine personal program. 
Type gzdrun help all once installed to see these options. Requires python3 and PySimpleGUI to be installed on your sistem. 
This program is really for my own usage, this is just here as a reference for myself, you can use it yourself, but the python application will see no further development due to the recent decisions of the PySimpleGUI API unintentionally 
throwing a wrench in the wheels of my plans. This was supposed to be a free application. It's code will remain open source.
The application automatically searches the steam directory, if present, for any IWADs, and the .config/gzdoom directory for any PWADs or PK3s.
      """,
      author='Sanguine Noctis',
      author_email='shotgunshellproducktions@gmail.com',
      url='https://github.com/ImpishDeathTech/GZDoomRun',
      platforms=["linux"],
      packages=['gzdoomrun'])
