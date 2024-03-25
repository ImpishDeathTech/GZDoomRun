#! /usr/bin/python3

import os, sys, subprocess, importlib.util

from types import ModuleType
from importlib.machinery import ModuleSpec
from pathlib import Path 

WAD_DIRECTORY     : str  = f"{Path.home()}/.config/gzdoom/"
VERSION_MAJOR     : int  = 1
VERSION_MINOR     : int  = 3
VERSION_PATCH     : int  = 1

CUSTOM_FILE       : dict = {
    "name": "custom",
    "path": f"{WAD_DIRECTORY}/custom.py"
}

HELP_STRING       : str = F"""
    GZDoom Run v{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH} Help
        
        GZDoom Run is a small linux program for loading GZDoom mods
        a little easier. This program is meant to be used with Steam 
        but can be used in standalone, and has a few command line options:
    
        help             
            prints this message

        with [keywords]   
            searches the mod directory for any WADs or PK3s resembling the
            provided keyword. This search is case sensitive, and is the default operation
            when no option keyword is provided.
        
        list
            Lists all of the currently available keywords.

        install [file names]
            if they exist, installs the provided WAD and PK3 files to GZdoom

        remove [keywords]
            if they exist, uninstalls the related WAD and PK3 files
"""


def load_custom():
    spec   : ModuleSpec = importlib.util.spec_from_file_location(CUSTOM_FILE["name"], CUSTOM_FILE["path"])
    custom : ModuleType = importlib.util.module_from_spec(spec)
    
    sys.modules[CUSTOM_FILE["name"]] = custom
    spec.loader.exec_module(custom)
    
    return custom


custom : ModuleType = load_custom()



class GZDoomRunError(Exception):

    def __init__(self, code: int, reason: str):
        self.__what__ : str = f"[GZDoom Run Error] ({code}): {reason}"
        self.__code__ : int = code
    
    def what(self):
        print(self.__what__)
        sys.exit(self.__code__)



def find_wad(wad_name: str) -> str:
    for file_name in os.listdir(WAD_DIRECTORY):
        if file_name.startswith(wad_name):
            print(file_name)
            return f"{WAD_DIRECTORY}{file_name}"

    return "nil"


def launch_gzdoom_with(wad_list: list):
    wad_list.insert(0, "gzdoom")
    result : CompletedProcess = subprocess.run(wad_list)
    
    if result.returncode == 0:
        print(result.stdout)

    else:
        print(result.stdout)
        raise GZDoomRunError(result.returncode, result.stderr)
    
    sys.exit(result.returncode)


def launch_gzdoom():
    launch_gzdoom_with([])


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
    
    def __init__(self, custom_options: dict):
        self.command_options : dict = {
            "help"   : self.print_help,
            "with"   : self.process_arguments
        }

        for key in custom_options.keys():
            self.command_options[key] = custom_options[key]


    def print_help(self, argc: int, argv: list):
        print(HELP_STRING)
        sys.exit(0)


    def process_arguments(self, argc: int, argv: list):
        if argc > 0:
            if argc <= 1:
                for option in self.command_options.keys():
                    if argv[0] == option:
                        key : str = argv[0]
                        argv.pop(0)
                        self.command_options[key](argc - 1, argv)
            elif argc == 1:
                print(argv[0])
                file_names : list = argv[0].split("%")
                file_paths : list = []

                for file_name in file_names:
                    file_path : str = find_wad(file_name)

                    if file_path != "nil":
                        file_paths.append(file_path)

                    else:
                        raise GZDoomRunError(2, f"No '{file_path}' .WAD or .PK3 found in {WAD_DIRECTORY}")
                    
                launch_gzdoom_with(file_paths)

            

        else:
            launch_gzdoom()



#######################################
#  MM    MM    AAA    IIIIII NN   NN  # 
#  MMM  MMM   AAAAA     II   NNNN NN  #
#  MMMMMMMM  AAA AAA    II   NN NNNN  #   
#  MM MM MM AAA   AAA IIIIII NN  NNN  #
#######################################
# Processes the arguments (if any),   #
# and either preforms the specified   #
# operation, runs a specified         #
# WAD/PK3 by filname (no suffix), or  #
# runs gzdoom as is with whatever     #
# IWADs are available.                #
#######################################

if __name__ == "__main__":
    options : CommandOptions = CommandOptions(custom.load_directory())

    try:
        sys.argv.pop(0)
        options.process_arguments(len(sys.argv), sys.argv)
    
    except GZDoomRunError as e:
        e.what()
