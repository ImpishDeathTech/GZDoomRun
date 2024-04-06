import os, sys, subprocess, importlib.util, json
import custom

from types import ModuleType
from importlib.machinery import ModuleSpec
from pathlib import Path
from custom import load_modcache 
from custom import save_modcache

modcache : dict = custom.load_modcache()

VERSION_MAJOR     : int  = modcache["version"][0]
VERSION_MINOR     : int  = modcache["version"][1]
VERSION_PATCH     : int  = modcache["version"][2]

del modcache

WAD_DIRECTORY : str = custom.WAD_DIRECTORY

class GZDoomRunError(Exception):

    def __init__(self, code: int, reason: str):
        self.__what__ : str = f"[GZDoom Run Error] ({code}): {reason}"
        self.__code__ : int = code
    
    def what(self, exit_app: bool=True):
        print(self.__what__)
        
        if exit_app:
            sys.exit(self.__code__)



def find_file(mod_name: str) -> str:
    for file_name in os.listdir(WAD_DIRECTORY):
        if file_name.startswith(mod_name) and file_name.endswith(custom.WAD_SUFFIXES):
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
                    warpmap : dict =  {
                        "E": None,
                        "M": None
                    }
                    E : bool = False 
                    M : bool = False
                    
                    pos += 1
                    s : str = argv[pos]

                    for c in s:
                        if M and c:
                            M = False
                            print(c)
                            warpmap["M"] = c
                            
                        elif warpmap["E"] and c:
                            E = False
                            print(c)
                            warpmap["E"] = c
                        
                        elif c.upper() == 'E':
                            print(c)
                            M = True

                        elif c.upper() == 'M':
                            print(c)
                            M = True

                    if warpmap["E"]:
                        iwad_path += ["-warp", warpmap["E"], warpmap["M"]]
                
                    else:
                        iwad_path += ["-warp", warpmap["M"]]

                    pos += 1

                    if pos == argc:
                        print(iwad_path + ["+dmflags", str(self.dmflags), "+dmflags2", str(self.dmflags2)])
                        return launch_gzdoom_with(iwad_path + ["+dmflags", str(self.dmflags), "+dmflags2", str(self.dmflags2)])
            
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
            launch_gzdoom()



