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
from gzdoomrun.utils import load_modcache, save_modcache, WAD_DIRECTORY

WAD_DIRECTORY    : str   = os.path.join(Path.home(), os.path.sep.join(modcache["path"]["config"]))

def main(argc: int, argv: list):
    modcache : dict = load_modcache()
    
    for key in modcache["manifest"].keys():
        if key == argv[0]:
            print(f"[GZDoom Run Uninstall]: Uninstalling {key} ...")
            main_directory : str = os.path.join(WAD_DIRECTORY, key)

            for file_path in modcache["manifest"][key]:
                print(f"[GZDoom Run Uninstall]: removing {file_path} ...")

                if file_path.endswith(".desktop"):
                    completed : CompletedProcess = subprocess.run(["sudo", "rm", file_path])

                    if completed.returncode != 0:
                        print(f"[GZDoom Run Error]({completed.returncode}): {completed.stderr}")
                        sys.exit(completed.returncode)
                
                elif os.path.isdir(file_path):
                    if file_path != main_directory:
                        os.rmdir(file_path)
                
                else:
                    try:
                        os.remove(file_path)

                    except PermissionError:
                        completed : CompletedProcess = subprocess.run(["sudo", "rm", file_path])

                        if completed.returncode != 0:
                            print(f"[GZDoom Run Error]({completed.returncode}): {completed.stdout}")
                            sys.exit(completed.returncode)

            if os.path.isdir(main_directory):
                os.rmdir(main_directory)
            
            del modcache["manifest"][key]
            save_modcache(modcache)
            print(f"[GZDoom Run Uninstall]: Uninstalled {key} successfully.")
            sys.exit(0)

    print(f"[GZDoom Run Error]: {argv[0]} not found!")
    sys.exit(1)