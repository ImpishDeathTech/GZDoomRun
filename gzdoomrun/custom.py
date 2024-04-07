import os

from gzdoomrun.utils import load_module, CUSTOM_DIRECTORY
from types import ModuleType

####################################################################
# This dictionary is loaded to the program dynamically at runtime  #
# Assign custom keywords to custom functions here                  #
# Note that if you would like the function to be included in help, #
# you must write your own help function to overwrite the built in  #
####################################################################

OPTIONS : dict = {}

####################################################################

def load_directory() -> dict:
    for file_name in os.listdir(CUSTOM_DIRECTORY):
        if file_name.endswith(".py"):
            modname : str        = file_name[:-3]
            modpath : str        = os.path.join(CUSTOM_DIRECTORY, file_name)
            module  : ModuleType = load_module(modname, modpath)

        OPTIONS[modname] : callable = module.main
    
    return OPTIONS
