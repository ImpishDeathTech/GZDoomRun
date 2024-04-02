# '''
# gzdoom.custom.uninstall.py
#
# BSD 2-Clause License  
# Copyright (c) 2024, Sanguine Noctis
#
# https://github.com/ImpishDeathTech/GZDoomRun/blob/master/LICENSE
# '''

import os, json, sys, subprocess, shutil

from pathlib import Path
from subprocess import CompletedProcess

MODCACHE_PATH    : str   = os.path.join(Path.home(), ".config", "gzdoom", "modcache.json")

def load_modcache() -> dict:
    with open(MODCACHE_PATH, "r") as f:
        data = json.load(f)
        return dict(data)

def save_modcache(data: dict):
    with open(MODCACHE_PATH, "w") as f:
        f.truncate()
        json.dump(data, f)

modcache : dict = load_modcache()

WAD_DIRECTORY    : str   = os.path.join(Path.home(), os.path.sep.join(modcache["path"]["config"]))

def main(argc: int, argv: list):
    for key in modcache["manifest"].keys():
        if key == argv[0]:
            main_directory : str = os.path.join(WAD_DIRECTORY, key)

            for file_path in modcache["manifest"][key]:
                if file_path.endswith(".desktop"):
                    completed : CompletedProcess = subprocess.run(["sudo", "rm", file_path])

                    if completed.returncode != 0:
                        print(f"[GZDoom Run Error]({completed.returncode}): {completed.stderr}")
                
                elif os.path.isdir(file_path):
                    if file_path != main_directory:
                        os.rmdir(file_path)
                
                else:
                    os.remove(file_path)
            
            if os.path.isdir(main_directory):
                os.rmdir(main_directory)
            
            del modcache["manifest"][key]
            save_modcache(modcache)
            sys.exit(0)

    print(f"[GZDoom Run Error]: {argv[0]} not found!")
    sys.exit(1)