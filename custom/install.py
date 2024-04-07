# '''
# gzdoom.custom.install.py
#
# BSD 2-Clause License  
# Copyright (c) 2024, Sanguine Noctis
#
# https://github.com/ImpishDeathTech/GZDoomRun/blob/master/LICENSE
# '''

import os, json, sys, subprocess, shutil

from pathlib import Path
from zipfile import ZipFile
from subprocess import CompletedProcess
from gzdoomrun.utils import load_modcache, save_modcache, WAD_DIRECTORY, STEAM_DIRECTORY, CUSTOM_DIRECTORY, WAD_SUFFIXES

APPS_DIRECTORY   : str   = os.path.join(os.path.sep, "usr", "share", "applications")
GZDOOM_DIRECTORY : str   = os.path.join(os.path.sep, "usr", "share", "gzdoom")
ARCHIVE_SUFFIXES : str   = (".pkz", ".zip") 
TEXT_SUFFIXES    : tuple = (".txt", ".otf", ".rtf")
GZDOOM_INSTALL   : str   = "[GZDoom Run Install]: "

IMAGE_NAMES      : tuple = (
    "artwork.png",
    "artwork.jpg",
    "banner.png",
    "banner.jpg",
    "logo.png",
    "icon.png"
) 

def install_desktop_file(zip_file: ZipFile, file_name: str):
    input_file = zip_file.open(file_name, "r")
    output_file = open(os.path.join(APPS_DIRECTORY, file_name.split(os.path.sep)[1]), "w")
    output_file.truncate()
    output_file.write(input_file)
    input_file.close()
    output_file.close()

def install_icon(temp_dir: str, file_name:str, icon_path: str, zip_file: ZipFile = None) -> dict:
    print(f"[GZDoom Run Install]: installing {file_name} to {icon_path}")

    name = file_name
    if zip_file:
        zip_file.extract(os.path.join(file_name))
    
    completed : CompletedProcess = subprocess.run(["sudo", "cp", os.path.join(temp_dir, file_name), icon_path])
                    
    if completed.returncode != 0:
        print(f"[GZDoom Run Error]({completed.returncode}): {completed.stdout}")
        sys.exit(completed.returncode)

def install_packet_archive(file_name: str):
    manifest : list = []
    outpath  : str  = os.path.join(WAD_DIRECTORY, file_name[:-4])
    icon_path: str  = os.path.join(os.path.sep, "usr", "share", "icons", file_name[:-4] + ".png")

    print(GZDOOM_INSTALL + f" {file_name} to {outpath} ...")

    if not os.path.isdir(outpath):
        os.makedirs(outpath)
    
    with ZipFile(file_name, mode='r', allowZip64=True) as zip_file:
        for name in zip_file.namelist():
            if name.endswith(WAD_SUFFIXES):
                print(f"[GZDoom Run Install]: insalling {name} to {os.path.join(WAD_DIRECTORY, name.split(os.path.sep)[1])} ...")
                manifest.append(os.path.join(WAD_DIRECTORY, name.split(os.path.sep)[1]))
                zip_file.extract(name)
                install_file(name.split(os.path.sep)[0], name.split(os.path.sep)[1], WAD_DIRECTORY)
            
            elif name.endswith(".desktop"):
                print(f"[GZDoom Run Install]: Installing {name} to {os.path.join(WAD_DIRECTORY, name)} ...")
                manifest.append(os.path.join(APPS_DIRECTORY, name.split(os.path.sep)[1]))
                zip_file.extract(name)
                install_file(name.split(os.path.sep)[0], name.split(os.path.sep)[1], APPS_DIRECTORY)
            
            elif name.endswith(TEXT_SUFFIXES):
                print(f"[GZDoom Run Install]: Installing {name} to {os.path.join(WAD_DIRECTORY, name)} ...")
                manifest.append(os.path.join(WAD_DIRECTORY, name))
                zip_file.extract(name, path=WAD_DIRECTORY) 
            
            elif name.endswith(IMAGE_NAMES):
                if name.endswith("icon.png"):
                    manifest.append(icon_path)
                    install_icon('./', name, icon_path, zip_file)

                else:
                    print(f"[GZDoom Run Install]: Installing {name} to {os.path.join(WAD_DIRECTORY, name)} ...")
                    manifest.append(os.path.join(WAD_DIRECTORY, name))
                    zip_file.extract(name, path=WAD_DIRECTORY)
    
    shutil.rmtree(file_name[:-4])
    modcache : dict = load_modcache()
    modcache["manifest"][file_name] = manifest 
    save_modcache(modcache)

    print(GZDOOM_INSTALL + f"{file_name} installed to {outpath} successfully")

def install_file(path: str, name: str, outpath: str):
    if name.endswith(".desktop"):
        completed : CompletedProcess = subprocess.run(["sudo", "cp", os.path.join(path, name), os.path.join(outpath, name)])
        
        if completed.returncode != 0:
            print(f"[GZDoom Run Error]{completed.returncode}: {completed.stderr}")
            sys.exit(completed.returncode)
    else:
        shutil.copy(os.path.join(path, name), os.path.join(outpath, name))

def install_packet_file(file_name: str):
    modcache : dict = load_modcache()
    outpath  : str  = os.path.join(WAD_DIRECTORY, file_name)

    print(f"{GZDOOM_INSTALL} {file_name} to {outpath} ...")

    result : CompletedProcess = subprocess.run(["cp", file_name, outpath])

    if result.returncode != 0:
        raise GZDoomRunError(result.returncode, result.stderr)
    
    else:
        save_manifest(file_name[:-4], [file_name])

    print(f"{GZDOOM_INSTALL} {file_name} installed to {outpath} successfully")
	

# gzdoom-run install [file names]
def main(argc: int, argv: list):
    for file_name in argv:
        if file_name.endswith(ARCHIVE_SUFFIXES):
            install_packet_archive(file_name)

        elif file_name.endswith(WAD_SUFFIXES):
            install_packet_file(file_name)

    sys.exit(0)