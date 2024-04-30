import os, sys, subprocess, importlib.util, json

from types import ModuleType
from importlib.machinery import ModuleSpec
from pathlib import Path
from gzdoomrun.error import GZDoomRunError
from gzdoomrun.dmflags import *

MODCACHE       : str   = os.path.join(Path.home(), ".config", "gzdoom", "modcache.json")

def load_modcache() -> dict:
    with open(MODCACHE, "r") as modcache: 
        data : dict = json.load(modcache)
        return data

def save_modcache(data: dict):
    with open(MODCACHE, "w") as modcache: 
        modcache.truncate()
        json.dump(data, modcache)

modcache : dict = load_modcache()

WAD_DIRECTORY     : str   = os.path.join(Path.home(), os.sep.join(modcache["path"]["config"]))
STEAM_DIRECTORY   : str   = os.path.join(Path.home(), os.sep.join(modcache["path"]["steam"]))
CUSTOM_DIRECTORY  : str   = os.path.join(WAD_DIRECTORY, "custom")
WAD_SUFFIXES      : tuple = (".wad", ".pk3")
GZDOOM_DIRECTORY  : str   = os.path.join(os.path.sep, "usr", "share", "gzdoom")
VERSION_MAJOR     : int  = modcache["version"][0]
VERSION_MINOR     : int  = modcache["version"][1]
VERSION_PATCH     : int  = modcache["version"][2]

# ''' 
# Names that will appear if the application 
# finds their associated files in the steam directory
# '''
STEAM_NAMES : dict = {
    "Doom": "doom1",
    "Doom (Unity)": "doom",
    "Doom 2": "DOOM2.WAD",
    "Doom 2 (Unity)": "doom2",
    "Final Doom: The Plutonia Experiment": "PLUTONIA.WAD",
    "Final Doom: TNT Evilution": "TNT.WAD",
    "The Ultimate Doom": "DOOM.WAD",
    "Heretic: Shadow of the Serpent Riders": "HERETIC.WAD",
    "Hexen: Beyond Heretic": "HEXEN.WAD",
    "Hexen: Deathkings of the Dark Citadel": "HEXDD.WAD",
    "Strife: Quest for the Sigil": "strife1",
    "Strife: Veteran Edition": "SVE.wad"
}

del modcache

# '''
# IWAD Finders
# 
# The following functions directly search for the 
# associated IWADs to ensure they have been installed
# through steam
# '''
def find_doom1() -> bool:
    doom_dir   : str = os.path.join(os.path.sep, "usr", "share", "doom")
    gzdoom_dir : str = os.path.join(os.path.sep, "usr", "share", "gzdoom")

    if os.path.isdir(doom_dir):
        return os.path.isfile(os.path.join(doom_dir, "doom1.wad"))
    
    elif os.path.isfile(os.path.join(gzdoom_dir, "doom1.wad")):
        return os.path.join(gzdoom_dir, "doom1.wad")
    
    return False

def find_doom2() -> bool:
    return os.path.isfile(os.path.join(STEAM_DIRECTORY, "Doom 2", "base", "DOOM2.WAD"))


def find_ultimate_doom() -> bool:
    return os.path.isfile(os.path.join(STEAM_DIRECTORY, "Ultimate Doom", "base", "DOOM.WAD"))

def find_heretic() -> bool:
    return os.path.isfile(os.path.join(STEAM_DIRECTORY, "Heretic Shadow of the Serpent Riders", "base", "HERETIC.WAD"))

def find_hexen() -> bool:
    return os.path.isfile(os.path.join(STEAM_DIRECTORY, "Hexen", "base", "HEXEN.WAD"))

def find_hexdd() -> bool:
    return os.path.isfile(os.path.join(STEAM_DIRECTORY, "Hexen Deathkings of the SerpentRiders", "base", "HEXDD.WAD"))

def find_strife1() -> bool:
    return os.path.isfile(os.path.join(STEAM_DIRECTORY, "Strife", "strife1.wad"))

def find_strife_veteran_edition() -> bool:
    return os.path.isfile(os.path.join(STEAM_DIRECTORY, "Strife", "SVE.wad"))


def finaldoom_find(iwad_name: str) -> bool:
    finaldoom_path : str = os.path.join(STEAM_DIRECTORY, "Doom 2", "finaldoombase")
    path           : str = os.path.join(finaldoom_path, f"{iwad_name}.WAD")
    
    if os.path.isdir(finaldoom_path):
        return os.path.isfile(path)


# '''
# This function will list IWADS based on what is installed
# to your .local/shared/Steam 
# '''
def load_iwads(folder_list: list) -> list:
    iwad_names : list = []
    
    keys = list(STEAM_NAMES.keys())

    if find_doom1():
        iwad_names.append(keys[0])

    for folder in folder_list:
        if folder == "Ultimate Doom" and find_ultimate_doom():
            iwad_names += [keys[1], keys[6]]
        
        elif folder == "Doom 2" and find_doom2():
            iwad_names += [keys[2], keys[3]]
            
            if finaldoom_find("PLUTONIA"):
                iwad_names.append(keys[4])

            if finaldoom_find("TNT"):
                iwad_names.append(keys[5])
        
        elif find_heretic():
            iwad_names.append(keys[7])
            
        elif find_hexen():
            iwad_names.append(keys[8])
        
        elif find_hexdd():
            iwad_names.append(keys[9])
        
        elif find_strife1():
            iwad_names.append(keys[10])
        
        elif find_strife_veteran_edition():
            iwad_names.append(keys[11])


    return iwad_names


def load_pwads(file_list: list) -> list:
    file_names : list = []

    for file_name in file_list:
        if os.path.isfile(os.path.join(WAD_DIRECTORY, file_name)) and file_name.lower().endswith(WAD_SUFFIXES):
            file_names.sort(key=str.lower)
            file_names.append(file_name[:-4])
    
    return file_names


def load_module(modname: str, modpath: str):
    spec   : ModuleSpec = importlib.util.spec_from_file_location(f"gzdoomrun.{modname}", modpath)
    custom : ModuleType = importlib.util.module_from_spec(spec)

    sys.modules[f"gzdoomrun.{modname}"] = custom
    spec.loader.exec_module(custom)

    return custom


def find_file(mod_name: str) -> str:
    for file_name in os.listdir(WAD_DIRECTORY):
        if file_name.startswith(mod_name) and file_name.endswith(WAD_SUFFIXES):
            return file_name

    return "nil"


def launch_gzdoom_with(wad_list: list) -> int:
    wad_list.insert(0, "gzdoom")
    print(wad_list)
    result : CompletedProcess = subprocess.run(wad_list)
    
    if result.returncode == 0:
        print(result.stdout)

    else:
        print(result.stdout)
        raise GZDoomRunError(result.returncode, result.stderr)
    
    return result.returncode


def launch_gzdoom() -> int:
    return launch_gzdoom_with([])


def load_filepaths(iwad_path: list, file_names: list) -> list:
    file_names = file_names
    file_paths : list = ["-file"]

    print(file_names)

    for file_name in file_names:
        file_path : str = find_file(file_name)

        if file_path != "nil":
            file_paths.append(file_path)

        else:
            raise GZDoomRunError(2, f"No '{file_path}.wad' or '{file_path}.pk3' found in {WAD_DIRECTORY}")
    
    print(iwad_path + file_paths)
    return iwad_path + file_paths


def parse_doom1_type(warp_map: str) -> list:
    o : list = warp_map.replace('E', ' ').replace('M', ' ').split(' ')
    return ['-warp', o[1], o[2]]


def parse_doom2_type(warp_map: str) -> list:
    if warp_map[3] == '0':
        return ['-warp', warp_map[4]]
    
    if ' ' in warp_map:
        return ['-warp', warp_map.replace(' ', '')[3:]]
    
    return ['-warp', warp_map[3:]]


def parse_warpmap(warp_map: str) -> list:
    if warp_map.startswith("MAP"):
        return parse_doom2_type(warp_map)

    return parse_doom1_type(warp_map)

#########################################
#        OOOOO PPPPP TTTTTT SSSSS       #
#        OO OO PP PP   TT   SS          #
#        OO OO PPPPP   TT   SSSSS       #
#        OO OO PP      TT      SS       #
#        OOOOO PP      TT   SSSSS       #
#########################################
# A set of functions to be called if    #
# their command line option is provided #
#########################################

class CommandOptions:  
    
    def __init__(self, custom_options: dict = {}):
        modcache : dict = load_modcache()

        self.dmflags         : int  = modcache["exec"]["dmflags"]
        self.dmflags2        : int  = modcache["exec"]["dmflags2"]
        self.command_options : dict = custom_options

    def process_arguments(self, argc: int, argv: list):
        if argc >= 2:
            iwad_path  : list = []
            pos        : int  = 0
            
            try:
                if argv[0] == "iwad":
                    iwad_path += ["-iwad", argv[1]]
                    pos += 2
                
                    if argc == 2:
                        return launch_gzdoom_with(["+dmflags", str(self.dmflags), "+dmflags2", str(self.dmflags2)] + iwad_path)
            
                if argv[pos] == "warp":
                    pos += 1
                    iwad_path += parse_warpmap(argv[pos])
                    pos += 1
            
                if argv[pos] == "skill":
                    iwad_path += ["-skill", argv[pos + 1]]
                    pos += 2
                
                    try:
                        a = argv[pos]
                        
                    except IndexError:
                        args = load_filepaths(iwad_path, []) + ["+dmflags", str(self.dmflags), "+dmflags2", str(self.dmflags2)]
                        return launch_gzdoom_with(args)

                if argv[pos] == "with":
                    args = load_filepaths(iwad_path, argv[pos + 1].split("%")) + ["+dmflags", str(self.dmflags), "+dmflags2", str(self.dmflags2)]
                    return launch_gzdoom_with(args)
                
                else:
                    for option in self.command_options.keys():
                        if argv[0] == option:
                            key : str = argv[0]
                            argv.pop(0)
                            self.command_options[key](argc - 1, argv)
                            
            except IndexError as err:
                print(err)

        else:
            return launch_gzdoom()

