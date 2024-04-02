#! /usr/bin/python3

import importlib.util, sys, os
import PySimpleGUI as gui 

from types import ModuleType
from importlib.machinery import ModuleSpec
from pathlib import Path

def load_gzdr() -> ModuleType:
    spec : ModuleSpec = importlib.util.spec_from_file_location("utils", os.path.join(Path.home(), ".config", "gzdoom", "gzdoomrunlib", "utils.py"))
    gzdr : ModuleType = importlib.util.module_from_spec(spec)

    sys.modules["utils"] = gzdr
    spec.loader.exec_module(gzdr)

    return gzdr

gzdr : ModuleType = load_gzdr()

# Event Names
DIRECTORY        : str = "@ Directory Path"
MOD_LIST         : str = "@ WAD/PK3 List"
IWAD_NAME        : str = "@ IWAD Name"
IWAD_LIST        : str = "@ IWAD List"
RUN_ARGS         : str = "@ Run Arguments"
ARTWORK          : str = "@ Game Artwork"
EXECUTE          : str = "@ Run GZDoom"
CLEAR_ARGS       : str = "@ Clear Arguments"
EXIT_APP         : str = "@ Exit Application"
WARP_MAP         : str = "@ Warp to Map"
DIFFICULTY       : str = "@ Set Difficulty"

# Colour Strings
BACKGROUND       : str = "#202020"
BUTTON_COLOR     : str = "#2B2B2B"
INPUT_BACKGROUND : str = "#4B4B4B"
TEXT_COLOR       : str = "#DFDFDF"
CLICK_BACKGROUND : str = "#3A3A3A"

# Path Strings
DEFAULT_PATH: str = gzdr.WAD_DIRECTORY
STEAM_PATH  : str = gzdr.custom.STEAM_DIRECTORY
ICON_PATH   : str = os.path.join(os.path.sep, "usr", "share", "icons", "gzdoom.png")

STEAM_NAMES : dict = {
    "Doom": "doom1",
    "Doom (Unity)": "doom",
    "Doom 2": "DOOM2.WAD",
    "Doom 2 (Unity)": "doom2",
    "Final Doom: The Plutonia Experiment": "PLUTONIA.WAD",
    "Final Doom: TNT Evilution": "TNT.WAD",
    "The Ultimate Doom": "DOOM.WAD",
    "Hexen: Beyond Heretic": "HEXEN.WAD"
}

# '''
# Application Object
# 
# Used to manage the state of the gui application
# '''
class Application:

    def __init__(self, title: str, iwad_table: list, pwad_table: list, launch_pad: list):
        self.title      : str                 = title
        self.is_running : bool                = True
        self.options    : gzdr.CommandOptions = gzdr.CommandOptions([])
        self.run_args   : str                 = ""
        self.iwad       : str                 = ""
        self.warp_map   : str                 = ""
        self.difficulty : str                 = ""

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
            EXIT_APP  : self.exit_application
        }

        self.layout : list = [
            [gui.Column([[gui.Frame("IWAD", background_color=BACKGROUND, layout=iwad_table)]], background_color=BACKGROUND)],
            [gui.Column([[gui.Frame("PWAD", background_color=BACKGROUND, layout=pwad_table)]], background_color=BACKGROUND)],
            [gui.Column([[gui.Frame("Launch", background_color=BACKGROUND, layout=launch_pad)]], background_color=BACKGROUND)]
        ]

        self.window       : gui.Window = gui.Window(title=self.title, icon=ICON_PATH, layout=self.layout, background_color=BACKGROUND)
        self.is_first_run : bool       = True
    
    def find(self, event: any) -> bool:
        for key in self.events.keys():
            if key == str(event):
                return True
        
        return False
    
    
    def execute(self, event: any, values: any):
        self.events[str(event)](event, values)


    def list_directory(self, event: any, values: any):
        folder = values[DIRECTORY]
        file_names: list = []
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        finally:
            for file_name in file_list:
                if os.path.isfile(os.path.join(folder, file_name)) and file_name.lower().endswith(gzdr.custom.WAD_SUFFIXES):
                    file_names.append(file_name[:-4])


    def update_run_args(self, event: any, values: any):
        try:
            file_name = os.path.join(values[DIRECTORY], values[MOD_LIST][0])
            run_args = values[RUN_ARGS].split(" ")
            run_args.append(values[MOD_LIST][0])
            self.run_args = "%".join(run_args)
            self.window[RUN_ARGS].update(" ".join(run_args))

        except:
            pass

    
    def update_arglist(self, event: any, values: any):
        if self.run_args:
            self.run_args += "%"
            self.run_args += "%".join(values[RUN_ARGS].split(" "))
        
        else:
            self.run_args += "%".join(values[RUN_ARGS].split(" "))


    def run_gzdoom(self, event: any, values: any):
        try:
            if not self.iwad:
                if not self.run_args:
                    self.options.process_arguments(0, [])
                else:
                    self.options.process_arguments(2, ["with", self.run_args])
            
            elif (self.iwad != "doom1") and self.run_args:
                if self.warp_map:
                    if self.difficulty:
                        self.options.process_arguments(6, ["iwad", self.iwad, "warp", self.warp_map, "skill", self.difficulty, "with", self.run_args])

                    else:
                        self.options.process_arguments(6, ["iwad", self.iwad, "warp", self.warp_map, "with", self.run_args])
                else:
                    self.options.process_arguments(4, ["iwad", self.iwad, "with", self.run_args])
                
            else:
                if self.warp_map:
                    if self.difficulty:
                        self.options.process_arguments(4, ["iwad", self.iwad, "warp", self.warp_map, "skill", self.difficulty])
                    
                    else:
                        self.options.process_arguments(4, ["iwad", self.iwad, "warp", self.warp_map])
                
                else:
                    self.options.process_arguments(2, ["iwad", self.iwad])
                
        
        except gzdr.GZDoomRunError as e:
            print(e.what(False))
        

    def clear_arguments(self, event: any, values: any):
        self.run_args   = ""
        self.warp_map   = ""
        self.difficulty = ""
        self.iwad       = ""
        self.window[RUN_ARGS].update("")
        self.window[WARP_MAP].update("")
        self.window[DIFFICULTY].update("")
        self.window[IWAD_NAME].update("")
        self.run_args = ""


    def exit_application(self, event: any, values: any):
        self.is_running = False

    
    def set_iwad(self, event: any, values: any):
        bignames : list = ["DOOM", "DOOM2", "HEXEN", "PLUTONIA", "TNT"]
        self.iwad = values[IWAD_NAME]

        if self.iwad in bignames:
            self.iwad += ".WAD"
        
        elif self.iwad in STEAM_NAMES.keys():
            self.iwad = STEAM_NAMES[self.iwad]

    
    def update_iwad(self, event: any, values: any):
        bignames : list = ["DOOM", "DOOM2", "HEXEN", "PLUTONIA", "TNT"]
        self.iwad = values[IWAD_LIST][0]
        
        if self.iwad in bignames:
            self.iwad += ".WAD"
        
        elif self.iwad in STEAM_NAMES.keys():
            self.iwad = STEAM_NAMES[self.iwad]
        
        if self.iwad.endswith(".WAD"):
            self.window[IWAD_NAME].update(self.iwad[:-4])
        
        else:
            self.window[IWAD_NAME].update(self.iwad)
    
    def set_warp_map(self, event: any, values: any):
        self.warp_map = values[WARP_MAP].upper()
        self.window[WARP_MAP].update(self.warp_map)
    
    def set_difficulty(self, event: any, values: any):
        self.difficulty = values[DIFFICULTY]
        self.window[DIFFICULTY].update(self.difficulty)
    

    def run(self):
        while self.is_running:
            e, v = self.window.read()

            if e == gui.WIN_CLOSED:
                break

            elif self.find(e):
                self.execute(e, v)

        self.window.close()

# '''
# Builds and returns the application based on the found iwads and pwads
# '''
def make_application(mod_list: list, iwad_list: list) -> Application:
    title      : str  = f"GZDoom Run v{gzdr.VERSION_MAJOR}.{gzdr.VERSION_MINOR}.{gzdr.VERSION_PATCH}"
    iwad_listln: int  = len(iwad_list)
    iwad_block : list = [
        [
            gui.Text("Path", size=(5, 1), background_color=BACKGROUND),
            gui.In(size=(23, 1), text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, enable_events=True, key=IWAD_NAME),
            gui.FolderBrowse(button_color=BUTTON_COLOR)
        ]
    ]
    pwad_block : list = [
        [
            gui.Text("Path", size=(5, 1), background_color=BACKGROUND),
            gui.In(DEFAULT_PATH, text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, size=(23, 1), enable_events=True, key=DIRECTORY),
            gui.FolderBrowse(button_color=BUTTON_COLOR)
        ],
        [gui.Listbox(mod_list, enable_events=True, text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, sbar_trough_color=CLICK_BACKGROUND, sbar_arrow_color=CLICK_BACKGROUND, sbar_background_color=BACKGROUND, size=(38, 8), key=MOD_LIST)]
    ]
    launch_pad : list = [
        [
            gui.Text("With", size=(5, 1), background_color=BACKGROUND),
            gui.In(size=(23, 1), text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, enable_events=True, key=RUN_ARGS),
            gui.Button("Run", size=(6, 1), button_color=BUTTON_COLOR, enable_events=True, key=EXECUTE)
        ],
        [
            gui.Text("Warp", size=(5, 1), background_color=BACKGROUND),
            gui.In(size=(23, 1), text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, enable_events=True, key=WARP_MAP),
            gui.Button("Clear", size=(6, 1), button_color=BUTTON_COLOR, enable_events=True, key=CLEAR_ARGS)
        ],
        [
            gui.Text("Skill", size=(5, 1), background_color=BACKGROUND),
            gui.In(size=(23, 1), text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, enable_events=True, key=DIFFICULTY),
            gui.Button("Exit", size=(6, 1), button_color=BUTTON_COLOR, enable_events=True, key=EXIT_APP)
        ]
    ]

    if iwad_listln > 0:
        if iwad_listln <= 8:
            iwad_block.append([gui.Listbox(iwad_list, text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, sbar_trough_color=CLICK_BACKGROUND, sbar_arrow_color=CLICK_BACKGROUND, sbar_background_color=BACKGROUND, enable_events=True, size=(38, iwad_listln), key=IWAD_LIST)])

        else:
            iwad_block.append([gui.Listbox(iwad_list, text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, sbar_trough_color=CLICK_BACKGROUND, sbar_arrow_color=CLICK_BACKGROUND, sbar_background_color=BACKGROUND, enable_events=True, size=(38, 8), key=IWAD_LIST)])

    return Application(title, iwad_block, pwad_block, launch_pad)

# '''
# IWAD Finders
# 
# The following functions directly search for the 
# associated IWADs to ensure they have been installed
# through steam
# '''
def find_doom1() -> bool:
    if os.path.isdir(os.path.join(os.path.sep, "usr", "share", "doom")):
        return os.path.isfile(os.path.join(os.path.sep, "usr", "share", "doom", "doom1.wad"))
    
    return False

def find_doom2() -> bool:
    return os.path.isfile(os.path.join(STEAM_PATH, "Doom 2", "base", "DOOM2.WAD"))


def find_ultimate_doom() -> bool:
    return os.path.isfile(os.path.join(STEAM_PATH, "Ultimate Doom", "base", "DOOM.WAD"))


def find_hexen() -> bool:
    return os.path.isfile(os.path.join(STEAM_PATH, "Hexen", "base", "HEXEN.WAD"))

def finaldoom_find(iwad_name: str) -> bool:
    finaldoom_path : str = os.path.join(STEAM_PATH, "Doom 2", "finaldoombase")
    plutonia_path  : str = os.path.join(finaldoom_path, f"{iwad_name}.WAD")
    if os.path.isdir(finaldoom_path):
        return os.path.isfile(plutonia_path)

def find_tnt() -> bool:
    finaldoom_path : str = os.path.join(STEAM_PATH, "Doom 2", "finaldoombase")
    tnt_path  : str = os.path.join(finaldoom_path, "TNT.WAD")
    if os.path.isdir(finaldoom_path):
        return os.path.isfile(tnt_path)

# '''
# This function will list IWADS based on what is installed
# to your .local/shared/Steam 
# '''
def load_iwads(folder_list: list) -> list:
    iwad_names : list = []
    keys       = list(STEAM_NAMES.keys())

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

        elif folder == "Hexen" and find_hexen():
            iwad_names.append(keys[7])

    return iwad_names


# '''
# This function will list PWADS and PK3s in the directory DEFAULT_PATH.
# This path can be changed dynamically by simply typing into
# the 'Mod Folder' input
# '''
def load_pwads(file_list: list) -> list:
    file_names : list = []

    for file_name in file_list:
        if os.path.isfile(os.path.join(DEFAULT_PATH, file_name)) and file_name.lower().endswith(gzdr.custom.WAD_SUFFIXES):
            file_names.sort(key=str.lower)
            file_names.append(file_name[:-4])
    
    return file_names

# '''
# This function will run the appliction without GUI
# and parse command line arguments
# '''
def run_from_cli(argc: int, argv: list) -> int:
    options : gzdr.CommandOptions = gzdr.CommandOptions(gzdr.custom.load_directory())
    
    try:
        argv.pop(0)
        options.process_arguments(argc - 1, argv)
    
    except gzdr.GZDoomRunError as e:
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
        pwad_names = load_pwads(file_list)
    
    try: 
        folder_list : list = os.listdir(STEAM_PATH)
    
    except:
        folder_list : list = []
    
    finally:
        iwad_names = load_iwads(folder_list)

    app : Application = make_application(pwad_names, iwad_names)
    app.run()



if __name__ == "__main__":
    if len(sys.argv) >= 3:
        sys.exit(run_from_cli(len(sys.argv), sys.argv))
        
    else:
        run_with_gui()
