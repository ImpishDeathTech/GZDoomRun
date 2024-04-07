#! /usr/bin/python3

# '''
# gzdoomrun.py
#
# BSD 2-Clause License  
# Copyright (c) 2024, Sanguine Noctis
#
# https://github.com/ImpishDeathTech/GZDoomRun/blob/master/LICENSE
# '''

import importlib.util, sys, os, string
import PySimpleGUI as gui 
import gzdoomrun.utils as utils

from gzdoomrun.dmflags import *
from types import ModuleType
from importlib.machinery import ModuleSpec
from pathlib import Path

from gzdoomrun.utils import CommandOptions
from gzdoomrun.custom import load_directory as load_custom_dir

# Event Names
DIRECTORY        : str = "@ Directory Path"
MOD_LIST         : str = "@ WAD/PK3 List"
IWAD_NAME        : str = "@ IWAD Name"
IWAD_LIST        : str = "@ IWAD List"
RUN_ARGS         : str = "@ Run Arguments"
ARTWORK          : str = "@ Game Artwork"
AUTOAIM          : str = "@ Autoaim"
EXECUTE          : str = "@ Run GZDoom"
CLEAR_ARGS       : str = "@ Clear Arguments"
EXIT_APP         : str = "@ Exit Application"
WARP_MAP         : str = "@ Warp to Map"
FREELOOK         : str = "@ Allow Freelook"
AUTOAIM          : str = "@ Allow Autoaim"
DIFFICULTY       : str = "@ Set Difficulty"
SET_DMFLAGS      : str = "@ Set DMFlags"
SET_DMFLAGS2     : str = "@ Set DMFlags 2"

# Colour Strings
BACKGROUND       : str = "#202020"
BUTTON_COLOR     : str = "#2B2B2B"
INPUT_BACKGROUND : str = "#4B4B4B"
TEXT_COLOR       : str = "#DFDFDF"
CLICK_BACKGROUND : str = "#3A3A3A"

# Path Strings
DEFAULT_PATH: str = utils.WAD_DIRECTORY
STEAM_PATH  : str = utils.STEAM_DIRECTORY
ICON_PATH   : str = os.path.join(os.path.sep, "usr", "share", "icons", "gzdoom.png")
STEAM_NAMES : list = utils.STEAM_NAMES

def evaluate(s: str):
    return eval(s)

# '''
# Application Object
# 
# Used to manage the state of the gui application
# '''
class Application:

    def __init__(self, title: str, iwad_table: list, pwad_table: list, launch_pad: list, dmflags: list, modcache: dict):
        self.title      : str            = title
        self.is_running : bool           = True
        self.options    : CommandOptions = CommandOptions(load_custom_dir())
        self.run_args   : str            = modcache["exec"]["with"]
        self.iwad       : str            = modcache["exec"]["iwad"]
        self.warp_map   : str            = modcache["exec"]["warp"]
        self.difficulty : str            = modcache["exec"]["skill"]
        self.dmflags    : str            = f"{self.options.dmflags}"
        self.dmflags2   : str            = f"{self.options.dmflags2}"

        self.events : dict = {
            DIRECTORY : self.list_directory,
            MOD_LIST  : self.update_run_args,
            IWAD_LIST : self.update_iwad,
            IWAD_NAME : self.set_iwad,
            RUN_ARGS  : self.update_arglist,
            EXECUTE   : self.run_gzdoom,
            WARP_MAP  : self.set_warp_map,
            DIFFICULTY: self.set_difficulty,
            CLEAR_ARGS: self.clear_arguments,
            EXIT_APP  : self.exit_application,
            SET_DMFLAGS : self.set_dmflags,
            SET_DMFLAGS2 : self.set_dmflags2
        }

        self.layout : list = [
            [gui.Column([[gui.Frame("IWAD", background_color=BACKGROUND, layout=iwad_table), gui.Frame("PWAD", background_color=BACKGROUND, layout=pwad_table)]], background_color=BACKGROUND)],
            [gui.Column([[gui.Frame("Launch", background_color=BACKGROUND, layout=launch_pad), gui.Frame("DMFlags", background_color=BACKGROUND, layout=dmflags)]], background_color=BACKGROUND)]
        ]

        self.window       : gui.Window = gui.Window(title=self.title, icon=ICON_PATH, layout=self.layout, background_color=BACKGROUND)
        self.is_first_run : bool       = True
    
    def find(self, event: str) -> bool:
        for key in self.events.keys():
            if key == str(event):
                return True
        
        return False
    
    
    def execute(self, event: str, values: list):
        self.events[str(event)](event, values)


    def set_dmflags(self, event: str, values: list):
        self.dmflags = values[event].upper().replace("-", "_")
        self.window[event].update(self.dmflags)
             

    def set_dmflags2(self, event: str, values: list):
        self.dmflags2 = values[event].upper().replace("-", "_")
        self.window[event].update(self.dmflags2)

    def list_directory(self, event: str, values: list):
        folder = values[event]
        file_names: list = []
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        finally:
            for file_name in file_list:
                if os.path.isfile(os.path.join(folder, file_name)) and file_name.lower().endswith(utils.WAD_SUFFIXES):
                    file_names.append(file_name[:-4])
                
            self.window[event].update(file_list)


    def update_run_args(self, event: str, values: list):
        self.run_args = "%".join([self.run_args, values[event][0]])
        
        if self.run_args[0] == '%':
            self.run_args = self.run_args[1:]

        self.window[RUN_ARGS].update(self.run_args)

    
    def update_arglist(self, event: str, values: list):
        self.run_args = values[event]
        self.window[event].update(self.run_args.replace(' ', '%'))


    def run_gzdoom(self, event: str, values: list):
        modcache : dict = utils.load_modcache()

        if self.dmflags.__contains__(" "):
            self.options.dmflags = eval(self.dmflags.replace(" ", " | "))
        
        else:
            self.options.dmflags = eval(self.dmflags)

        if self.dmflags2.__contains__(" "):
            self.options.dmflags2 = eval(self.dmflags2.replace(" ", " | "))
        
        else:
            self.options.dmflags2 = eval(self.dmflags2)
        
        modcache["exec"]["dmflags"]  = self.options.dmflags
        modcache["exec"]["dmflags2"] = self.options.dmflags2
        
        utils.save_modcache(modcache)

        try:
            if not self.iwad:
                if not self.run_args:
                    self.options.process_arguments(0, [])
                else:
                    self.options.process_arguments(2, ["with", self.run_args])
            
            elif (self.iwad != "doom1") and self.run_args:
                if self.warp_map:
                    if self.difficulty:
                        self.options.process_arguments(8, ["iwad", self.iwad, "warp", self.warp_map, "skill", self.difficulty, "with", self.run_args])

                    else:
                        self.options.process_arguments(6, ["iwad", self.iwad, "warp", self.warp_map, "with", self.run_args])
                else:
                    self.options.process_arguments(4, ["iwad", self.iwad, "with", self.run_args])
                
            else:
                if self.warp_map:
                    if self.difficulty:
                        self.options.process_arguments(6, ["iwad", self.iwad, "warp", self.warp_map, "skill", self.difficulty])
                    
                    else:
                        self.options.process_arguments(4, ["iwad", self.iwad, "warp", self.warp_map])
                
                else:
                    self.options.process_arguments(2, ["iwad", self.iwad])
                
        
        except utils.GZDoomRunError as exn:
            print(exn.what(False))
        

    def clear_arguments(self, event: str, values: list):
        modcache : dict = utils.load_modcache()
        
        modcache["exec"]["iwad"]     = ""
        modcache["exec"]["warp"]     = ""
        modcache["exec"]["skill"]    = ""
        modcache["exec"]["with"]     = ""
        modcache["exec"]["dmflags"]  = 0
        modcache["exec"]["dmflags2"] = 0
        
        utils.save_modcache(modcache)

        self.run_args         = ""
        self.warp_map         = ""
        self.difficulty       = ""
        self.iwad             = ""
        self.dmflags          = "0"
        self.dmflags2         = "0"
        self.options.dmflags  = 0
        self.options.dmflags2 = 0

        self.window[RUN_ARGS].update("")
        self.window[WARP_MAP].update("")
        self.window[DIFFICULTY].update("")
        self.window[IWAD_NAME].update("")
        self.window[SET_DMFLAGS].update("0")
        self.window[SET_DMFLAGS2].update("0")


    def exit_application(self, event: str, values: list):
        modcache : dict = utils.load_modcache()

        if self.dmflags.__contains__(" "):
            self.options.dmflags = eval(self.dmflags.replace(" ", " | ").replace("$", "0x").replace("#", ""))
        
        else:
            self.options.dmflags = eval(self.dmflags)

        if self.dmflags2.__contains__(" "):
            self.options.dmflags2 = eval(self.dmflags2.replace(" ", " | ").replace("$", "0x").replace("#", ""))
        
        else:
            self.options.dmflags2 = eval(self.dmflags2)
        
        modcache["exec"]["dmflags"]  = self.options.dmflags
        modcache["exec"]["dmflags2"] = self.options.dmflags2
        
        utils.save_modcache(modcache)
        self.is_running = False

    
    def set_iwad(self, event: str, values: list):
        bignames : list = ["DOOM", "DOOM2", "HEXEN", "PLUTONIA", "TNT"]
        modcache : dict = utils.load_modcache()
        
        self.iwad = values[event]

        if self.iwad in bignames:
            self.iwad += ".WAD"
        
        elif self.iwad in STEAM_NAMES.keys():
            self.iwad = STEAM_NAMES[self.iwad]

        modcache["exec"]["iwad"] = self.iwad
        utils.save_modcache(modcache)

    
    def update_iwad(self, event: str, values: list):
        bignames : list = ["DOOM", "DOOM2", "HEXEN", "PLUTONIA", "TNT"]
        modcache : dict = utils.load_modcache()

        self.iwad = values[event][0]
        
        if self.iwad in bignames:
            self.iwad += ".WAD"
        
        elif self.iwad in STEAM_NAMES.keys():
            self.iwad = STEAM_NAMES[self.iwad]
        
        if self.iwad.endswith(".WAD"):
            self.window[IWAD_NAME].update(self.iwad[:-4])
        
        else:
            self.window[IWAD_NAME].update(self.iwad)

        modcache["exec"]["iwad"] = self.iwad
        utils.save_modcache(modcache)
    
    
    def set_warp_map(self, event: str, values: list):
        modcache : dict = utils.load_modcache()
        
        self.warp_map = values[event].upper()
        self.window[event].update(self.warp_map)

        modcache["exec"]["warp"] = self.warp_map
        utils.save_modcache(modcache)
    

    def set_difficulty(self, event: str, values: list):
        modcache : dict = utils.load_modcache()
        print(f"[GZDoom Run]: Setting Difficulty to {values[event]}")
        self.difficulty = values[event]
        self.window[event].update(self.difficulty)
        
        modcache["exec"]["skill"] = self.difficulty
        utils.save_modcache(modcache)
    

    def run(self):
        while self.is_running:
            e, v = self.window.read()

            if e == gui.WIN_CLOSED:
                break

            elif self.find(str(e)):
                self.execute(str(e), v)

        self.window.close()

# '''
# Builds and returns the application based on the found iwads and pwads
# '''
def make_application(mod_list: list, iwad_list: list) -> Application:
    modcache   : dict = utils.load_modcache()
    title      : str  = f"GZDoom Run v{utils.VERSION_MAJOR}.{utils.VERSION_MINOR}.{utils.VERSION_PATCH}"
    iwad_listln: int  = len(iwad_list)
    iwad_name  : str  = modcache["exec"]["iwad"]
        
    if iwad_name.endswith(".WAD"):
        iwad_name = iwad_name[:-4]
    
    iwad_block : list = [
        [
            gui.Text("Path", size=(5, 1), background_color=BACKGROUND),
            gui.In(iwad_name, size=(23, 1), text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, enable_events=True, key=IWAD_NAME),
            gui.FolderBrowse(button_color=BUTTON_COLOR)
        ]
    ]
    pwad_block : list = [
        [
            gui.Text("Path", size=(5, 1), background_color=BACKGROUND),
            gui.In(utils.WAD_DIRECTORY, text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, size=(23, 1), enable_events=True, key=DIRECTORY),
            gui.FolderBrowse(button_color=BUTTON_COLOR)
        ],
        [gui.Listbox(mod_list, enable_events=True, text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, 
            sbar_trough_color=CLICK_BACKGROUND, sbar_arrow_color=CLICK_BACKGROUND, sbar_background_color=BACKGROUND, size=(38, 8), key=MOD_LIST)]
    ]
    launch_pad : list = [
        [
            gui.Text("With", size=(5, 1), background_color=BACKGROUND),
            gui.In(modcache["exec"]["with"], size=(23, 1), text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, enable_events=True, key=RUN_ARGS),
            gui.Button("Run", size=(6, 1), button_color=BUTTON_COLOR, enable_events=True, key=EXECUTE)
        ],
        [
            gui.Text("Warp", size=(5, 1), background_color=BACKGROUND),
            gui.In(modcache["exec"]["warp"], size=(23, 1), text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, enable_events=True, key=WARP_MAP),
            gui.Button("Clear", size=(6, 1), button_color=BUTTON_COLOR, enable_events=True, key=CLEAR_ARGS)
        ],
        [
            gui.Text("Skill", size=(5, 1), background_color=BACKGROUND),
            gui.In(modcache["exec"]["skill"], size=(23, 1), text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, enable_events=True, key=DIFFICULTY),
            gui.Button("Exit", size=(6, 1), button_color=BUTTON_COLOR, enable_events=True, key=EXIT_APP)
        ]
    ]

    dmflags_layout : list = [
            [gui.Frame("dmflags", background_color=BACKGROUND, p=3, layout=[[gui.In(str(modcache["exec"]["dmflags"]), size=(39, 1), 
                text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, enable_events=True, key=SET_DMFLAGS)]])],
            [gui.Frame("dmflags2", background_color=BACKGROUND, p=3, layout=[[gui.In(str(modcache["exec"]["dmflags2"]), size=(39, 1), 
                text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, enable_events=True, key=SET_DMFLAGS2)]])]
    ]

    if iwad_listln > 0:
        if iwad_listln <= 8:
            iwad_block.append([gui.Listbox(iwad_list, text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, 
                sbar_trough_color=CLICK_BACKGROUND, sbar_arrow_color=CLICK_BACKGROUND, sbar_background_color=BACKGROUND, 
                enable_events=True, size=(38, iwad_listln), key=IWAD_LIST)])

        else:
            iwad_block.append([gui.Listbox(iwad_list, text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, 
                sbar_trough_color=CLICK_BACKGROUND, sbar_arrow_color=CLICK_BACKGROUND, sbar_background_color=BACKGROUND, 
                enable_events=True, size=(38, 8), key=IWAD_LIST)])

    return Application(title, iwad_block, pwad_block, launch_pad, dmflags_layout, modcache)



# '''
# This function will run the appliction without GUI
# and parse command line arguments
# '''
def run_from_cli(argc: int, argv: list) -> int:
    options : CommandOptions = CommandOptions(load_custom_dir())
    
    try:
        argv.pop(0)
        options.process_arguments(argc - 1, argv)
    
    except utils.GZDoomRunError as e:
        e.what()
        return 1
    
    return 0

# '''
# This function will launch the GUI application
# '''
def run_with_gui():
    try:
        file_list : list = os.listdir(DEFAULT_PATH)
    
    except:
        file_list : list = []
    
    finally:
        pwad_names = utils.load_pwads(file_list)
    
    try: 
        folder_list : list = os.listdir(STEAM_PATH)
    
    except:
        folder_list : list = []
    
    finally:
        iwad_names = utils.load_iwads(folder_list)

    app : Application = make_application(pwad_names, iwad_names)
    app.run()

import sys


def is_venv():
    return (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

# '''
# Main Block
# '''
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        sys.exit(run_from_cli(len(sys.argv), sys.argv))

    elif len(sys.argv) == 2:
        if sys.argv[1] == "is-venv":
            if is_venv():
                sys.exit(0)
            else:
                sys.exit(1)
        else:
            sys.exit(run_from_cli(len(sys.argv), sys.argv))
    else:
        run_with_gui()
