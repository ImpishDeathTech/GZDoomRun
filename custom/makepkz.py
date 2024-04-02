# '''
# gzdoom.custom.makepkz.py
#
# BSD 2-Clause License  
# Copyright (c) 2024, Sanguine Noctis
#
# https://github.com/ImpishDeathTech/GZDoomRun/blob/master/LICENSE
# '''

import os, json, sys

from pathlib import Path
from zipfile import ZipFile

WAD_SUFFIXES  : tuple = (".wad", ".pk3")
TEXT_SUFFIXES : tuple = (".txt", ".otf", ".rtf", ".desktop")
IMAGE_NAMES: tuple = (
    "icon.png",
    "logo.png",
    "banner.png", 
    "artwork.png",  
    "banner.jpg",
    "artwork.jpg"
)

def main(argc: int, argv: list):
    for path_name in argv:
        if os.path.isdir(path_name):
            with ZipFile(path_name + ".pkz", mode="w", allowZip64=True) as zip_file:
                for file_name in os.listdir(path_name):
                    if file_name.endswith(WAD_SUFFIXES) or file_name.endswith(TEXT_SUFFIXES) or (file_name in IMAGE_NAMES):
                        print(f"[GZdoom Run]->(Make PKZ): adding {file_name} to {path_name}.pkz ...")
                        zip_file.write(os.path.join(path_name, file_name))
        else:
            print(f"[GZDoom Run Error]->(Make PKZ): Invalid Path {path_name}")
            sys.exit(1)
    
    print(zip_file.namelist())
    sys.exit(0)
