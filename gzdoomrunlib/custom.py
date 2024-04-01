import os, sys, importlib.util, subprocess, json

from types import ModuleType
from importlib.machinery import ModuleSpec
from pathlib import Path 

WAD_DIRECTORY  : str   = os.path.join(Path.home(), ".config", "gzdoom")
CUSTOM_DIR     : str   = os.path.join(WAD_DIRECTORY, "custom")
MODCACHE       : str   = os.path.join(WAD_DIRECTORY, "modcache.json")
WAD_SUFFIXES   : tuple = (".wad", ".pk3")
GZDOOM_INSTALL : str   = "[GZDoom Run Install]: "
GZDOOM_REMOVE  : str   = "[GZDoom Run Removal]: "

def load_module(modname: str, modpath: str):
    spec   : ModuleSpec = importlib.util.spec_from_file_location(modname, modpath)
    custom : ModuleType = importlib.util.module_from_spec(spec)

    sys.modules[modname] = custom
    spec.loader.exec_module(custom)

    return custom


###################################################
#     CCC  UU UU  SSSSS TTTTTT  OOO  MM    MM     #
#    CC CC UU UU SS       TT   OO OO MMM  MMM     #
#    CC    UU UU  SSSS    TT   OO OO MMMMMMMM     #
#    CC CC UU UU     SS   TT   OO OO MM MM MM     #
#     CCC   UUU  SSSSS    TT    OOO  MM    MM     #
###################################################
# Define any custom command options in this file  #
# as shown below and assign them in the OPTIONS   #
# dictionary at the bottom of the file            #
# Alternatively, you can define it in their own   #
# file in the CUSTOM_DIR if you need more room    #
# to breathe. Only define small commands here.    #
###################################################

def list_wads(argc: int, argv: list):
    wad_list : list = os.listdir(WAD_DIRECTORY)
    wad_list.sort(key=str.lower)

    for file_name in wad_list:
        if file_name.endswith(WAD_SUFFIXES):
            print(file_name[:-4])
    
    sys.exit(0)

# gzdoom-run remove [keywords]
def remove_wads(argc: int, argv: list):
    for file_name in os.listdir(WAD_DIRECTORY):
        for i in range(argc):
            if file_name.startswith(argv[i]) and file_name.endswith(WAD_SUFFIXES):
                print(GZDOOM_REMOVE + f"Uninstalling {file_name} ...")
                result : CompletedProcess = subprocess.run(["rm", WAD_DIRECTORY + file_name])
                if result.returncode != 0:
                    raise GZDoomRunError(result.returncode, result.stderr)
                
                print(GZDOOM_REMOVE + f"{file_name} uninstalled successfully")
	
    sys.exit(0)


####################################################################
# This dictionary is loaded to the program dynamically at runtime  #
# Assign custom keywords to custom functions here                  #
# Note that if you would like the function to be included in help, #
# you must write your own help function to overwrite the built in  #
####################################################################

OPTIONS : dict = {
    "list"      : list_wads,
    "uninstall" : remove_wads,
}

####################################################################

def suffixes() -> tuple:
    return WAD_SUFFIXES

def load_directory() -> dict:
    for file_name in os.listdir(CUSTOM_DIR):
        if file_name.endswith(".py"):
            modname : str        = file_name[:-3]
            modpath : str        = CUSTOM_DIR + file_name
            module  : ModuleType = load_module(modname, modpath)

        OPTIONS[modname] : callable = module.main
    
    return OPTIONS
