# '''
# gzdoom.custom.install.py
#
# BSD 2-Clause License  
# Copyright (c) 2024, Sanguine Noctis
#
# https://github.com/ImpishDeathTech/GZDoomRun/blob/master/LICENSE
# '''

import os, json, sys, shutil, subprocess

from pathlib import Path
from zipfile import ZipFile


MODCACHE_PATH    : str   = os.path.join(Path.home(), ".config", "gzdoom", "modcache.json")

def load_modcache() -> dict:
    with open(MODCACHE_PATH, "r") as f:
        data = json.load(f)
        return dict(data)


def save_modcache(data: dict):
    with open(MODCACHE_PATH, "w") as f:
        f.truncate()
        json.dump(data, f)

def save_manifest(name: str, manifest: list):
    modcache : dict = load_modcache()
    modcache["manifest"][name] = manifest
    save_modcache(modcache)

modcache : dict = load_modcache()

WAD_DIRECTORY    : str   = os.path.join(Path.home(), os.path.sep.join(modcache["path"]["config"]))
STEAM_DIRECTORY  : str   = os.path.join(Path.home(), os.path.sep.join(modcache["path"]["steam"]))
CUSTOM_DIRECTORY : str   = os.path.join(WAD_DIRECTORY, "custom")
APPS_DIRECTORY   : str   = os.path.join(os.path.sep, "usr", "share", "applications")
GZDOOM_DIRECTORY : str   = os.path.join(os.path.sep, "usr", "share", "gzdoom")
ARCHIVE_SUFFIXES : str   = (".pkz", ".zip") 
WAD_SUFFIXES     : tuple = (".wad", "pk3")
TEXT_SUFFIXES    : tuple = (".txt", ".otf", ".rtf")
GZDOOM_INSTALL   : str   = "[GZDoom Run Install]: "

del modcache

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

def install_packet_archive(file_name: str):
    manifest : list = []
    outpath  : str  = os.path.join(WAD_DIRECTORY, file_name[:-4])

    print(GZDOOM_INSTALL + f" {file_name} to {outpath} ...")

    if not os.path.isdir(outpath):
        manifest.append(outpath)
        os.makedirs(outpath)
    
    with ZipFile(file_name, mode='r', allowZip64=True) as zip_file:
        for name in zip_file.namelist():
            if name.endswith(WAD_SUFFIXES):
                print(f"[GZDoom Run Install]: insalling {name} to {os.path.join(WAD_DIRECTORY, name.split(os.path.sep)[1])} ...")
                manifest.append(os.path.join(WAD_DIRECTORY, name))
                zip_file.extract(name)
                install_file(name.split(os.path.sep)[0], name.split(os.path.sep)[1], WAD_DIRECTORY)
            
            elif name.endswith(".desktop"):
                print(f"[GZDoom Run Install]: Installing {name} to {os.path.join(WAD_DIRECTORY, name)} ...")
                manifest.append(os.path.join(APPS_DIRECTORY, name))
                zip_file.extract(name)
                install_file(name.split(os.path.sep)[0], name.split(os.path.sep)[1], APPS_DIRECTORY)
            
            elif name.endswith(TEXT_SUFFIXES):
                print(f"[GZDoom Run Install]: Installing {name} to {os.path.join(WAD_DIRECTORY, name)} ...")
                manifest.append(os.path.join(WAD_DIRECTORY, name))
                zip_file.extract(name, path=WAD_DIRECTORY) 
            
            elif name.endswith(IMAGE_NAMES):
                print(f"[GZDoom Run Install]: Installing {name} to {os.path.join(WAD_DIRECTORY, name)} ...")
                manifest.append(os.path.join(WAD_DIRECTORY, name))
                zip_file.extract(name, path=WAD_DIRECTORY)
    
    shutil.rmtree(file_name[:-4])
    save_manifest(file_name[:-4], manifest)

    print(GZDOOM_INSTALL + f"{file_name} installed to {outpath} successfully")

def install_file(path: str, name: str, outpath: str):
    if name.endswith(".desktop"):
        subprocess.run(["sudo", "cp", os.path.join(path, name), os.path.join(outpath, name)])
    else:
        shutil.copy(os.path.join(path, name), os.path.join(outpath, name))

def install_packet_directory(path: str):
    manifest : list = []
    outpath  : str  = os.path.join(WAD_DIRECTORY, path)

    print(GZDOOM_INSTALL + f" {file_name} to {outpath} ...")

    if not os.path.isdir(outpath):
        manifest.append(outpath)
        os.makedirs(outpath)
    
    for name in os.listdir(path):
        if name.endswith(WAD_SUFFIXES):
            print(name)
            manifest.append(os.path.join(WAD_DIRECTORY, name))
            install_file(path, name, WAD_DIRECTORY)
            
        elif name.endswith(".desktop"):
            print(name)
            manifest.append(os.path.join(APPS_DIRECTORY, name))
            install_file(path, name, APPS_DIRECTORY)
            
        elif name.endswith(TEXT_SUFFIXES):
            print(name)
            manifest.append(os.path.join(outpath, name))
            install_file(path, name, outpath)
            
        elif name.endswith(IMAGE_NAMES):
            print(name)
            manifest.append(os.path.join(outpath, name))
            install_file(path, name, outpath)
    
    save_manifest(path, manifest)

    print(GZDOOM_INSTALL + f"{file_name} installed to {outpath} successfully")

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