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

from types import ModuleType
from importlib.machinery import ModuleSpec
from pathlib import Path
import utils as gzdr
from utils import CommandOptions

# '''
# Loads the library dinamically because I wrote this weird. 
# It was never supposed to be this complex. ^,..,^"
# ''' 
'''
def load_gzdr() -> ModuleType:
    spec : ModuleSpec = importlib.util.spec_from_file_location("utils", os.path.join(Path.home(), ".config", "gzdoom", "gzdoomrunlib", "utils.py"))
    gzdr : ModuleType = importlib.util.module_from_spec(spec)

    sys.modules["utils"] = gzdr
    spec.loader.exec_module(gzdr)

    return gzdr

gzdr : ModuleType = load_gzdr()

CommandOptions = gzdr.CommandOptions
'''


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
DEFAULT_PATH: str = gzdr.WAD_DIRECTORY
STEAM_PATH  : str = gzdr.custom.STEAM_DIRECTORY
ICON_PATH   : str = os.path.join(os.path.sep, "usr", "share", "icons", "gzdoom.png")

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
    "Hexen: Beyond Heretic": "HEXEN.WAD"
}

# DMFlags
ALLOW_HEALTH        : int = 0x00000001
ALLOW_POWERUPS      : int = 0x00000002
WEAPONS_STAY        : int = 0x00000004
FALL_DMG            : int = 0x00000008
FALL_DMG_HEXEN      : int = 0x00000010
FALL_DMG_STRIFE     : int = 0x00000018
SAME_MAP            : int = 0x00000040
SPAWN_FARTHEST      : int = 0x00000080
FORCE_RESPAWN       : int = 0x00000100
ALLOW_ARMOR         : int = 0x00000200
ALLOW_EXIT          : int = 0x00000400
INFINITE_AMMO       : int = 0x00000800
NO_MONSTERS         : int = 0x00001000
MONSTERS_RESPAWN    : int = 0x00002000
ITEMS_RESPAWN       : int = 0x00004000
FAST_MONSTERS       : int = 0x00008000
ALLOW_JUMP          : int = 0x00010000
ALLOW_FREELOOK_OFF  : int = 0x00040000
ALLOW_FREELOOK      : int = 0x00080000
ALLOW_FOV           : int = 0x00100000
SPAWN_MULTI_WEAPONS : int = 0x00200000
ALLOW_CROUCH        : int = 0x00400000
LOOSE_INVENTORY     : int = 0x01000000
KEEP_KEYS           : int = 0x02000000
KEEP_WEAPONS        : int = 0x04000000
KEEP_ARMOR          : int = 0x08000000
KEEP_POWERUPS       : int = 0x10000000
KEEP_AMMO           : int = 0x20000000
LOSE_HALF_AMMO      : int = 0x40000000

DMFLAGS_DEFAULT : int = (
    ALLOW_HEALTH | 
    ALLOW_POWERUPS | 
    ALLOW_ARMOR | 
    ALLOW_EXIT | 
    ALLOW_JUMP | 
    ALLOW_FOV | 
    SPAWN_MULTI_WEAPONS | 
    ALLOW_CROUCH | 
    KEEP_KEYS | 
    KEEP_WEAPONS | 
    KEEP_ARMOR | 
    KEEP_POWERUPS | 
    KEEP_AMMO
)

# DMFlags 2
DROP_WEAPON                     : int = 0x00000002
NO_TEAM_CHANGING                : int = 0x00000010
DOUBLE_AMMO                     : int = 0x00000040
DEGENERATION_ON                 : int = 0x00000080
ALLOW_BFG_AIMING                : int = 0x00000100
BARRELS_RESPAWN                 : int = 0x00000200
RESPAWN_PROTECTION              : int = 0x00000400
SPAWN_WHERE_DIED                : int = 0x00001000
KEEP_FRAGS_GAINED               : int = 0x00002000
NO_RESPAWN                      : int = 0x00004000
LOSE_FRAG_ON_DEATH              : int = 0x00008000
INFINITE_INVENTORY              : int = 0x00010000
NO_MONSTERS_TO_EXIT             : int = 0x00020000
ALLOW_AUTOMAP                   : int = 0x00040000
AUTOMAP_ALLIES                  : int = 0x00080000
ALLOW_SPYING                    : int = 0x00100000
CHASECAM_CHEAT                  : int = 0x00200000
DISALLOW_SUICIDE                : int = 0x00400000
ALLOW_AUTOAIM                   : int = 0x00800000
CHECK_AMMO_FOR_WEAPON_SWITCH    : int = 0x01000000
ICON_OF_SINS_DEATH_KILLS_SPAWNS : int = 0x02000000
END_SECTOR_COUNTS_FOR_KILLS     : int = 0x04000000
BIG_POWERUPS_RESPAWN            : int = 0x08000000
ALLOW_VERTICAL_BULLET_SPREAD    : int = 0x40000000

DMFLAGS2_DEFAULT                : int = (
    ALLOW_BFG_AIMING | 
    ALLOW_AUTOMAP | 
    AUTOMAP_ALLIES | 
    ALLOW_SPYING |
    CHECK_AMMO_FOR_WEAPON_SWITCH | 
    ICON_OF_SINS_DEATH_KILLS_SPAWNS | 
    END_SECTOR_COUNTS_FOR_KILLS
)

# '''
# Application Object
# 
# Used to manage the state of the gui application
# '''
class Application:

    def __init__(self, title: str, iwad_table: list, pwad_table: list, launch_pad: list, dmflags: list, modcache: dict):
        self.title      : str            = title
        self.is_running : bool           = True
        self.options    : CommandOptions = CommandOptions()
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
    
    def find(self, event: any) -> bool:
        for key in self.events.keys():
            if key == str(event):
                return True
        
        return False
    
    
    def execute(self, event: any, values: any):
        self.events[str(event)](event, values)


    def set_dmflags(self, event: any, values: any):
        self.dmflags = values[SET_DMFLAGS].upper().replace("-", "_")
        self.window[SET_DMFLAGS].update(self.dmflags)
             

    def set_dmflags2(self, event: any, values: any):
        self.dmflags2 = values[SET_DMFLAGS2].upper().replace("-", "_")
        self.window[SET_DMFLAGS2].update(self.dmflags2)

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
        modcache : dict = gzdr.load_modcache()

        if self.dmflags.__contains__(" "):
            self.options.dmflags = eval(self.dmflags.replace(" ", " | "))
        
        else:
            self.options.dmflags = eval(self.dmflags)

        if self.dmflags2.__contains__(" "):
            self.options.dmflags2 = eval(self.dmflags2.replace(" ", " | "))
        
        else:
            self.options.dmflags2 = eval(self.dmflags2)
        
        modcache["exec"]["dmflags"] = self.options.dmflags
        modcache["exec"]["dmflags2"] = self.options.dmflags2
        
        gzdr.save_modcache(modcache)

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
                
        
        except gzdr.GZDoomRunError as e:
            print(e.what(False))
        

    def clear_arguments(self, event: any, values: any):
        modcache : dict = gzdr.load_modcache()
        
        modcache["exec"]["iwad"]  = ""
        modcache["exec"]["warp"]  = ""
        modcache["exec"]["skill"] = ""
        modcache["exec"]["with"]  = ""
        
        gzdr.custom.save_modcache(modcache)

        self.run_args   = ""
        self.warp_map   = ""
        self.difficulty = ""
        self.iwad       = ""

        self.window[RUN_ARGS].update("")
        self.window[WARP_MAP].update("")
        self.window[DIFFICULTY].update("")
        self.window[IWAD_NAME].update("")




    def exit_application(self, event: any, values: any):
        modcache : dict = gzdr.load_modcache()

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
        
        gzdr.save_modcache(modcache)
        self.is_running = False

    
    def set_iwad(self, event: any, values: any):
        bignames : list = ["DOOM", "DOOM2", "HEXEN", "PLUTONIA", "TNT"]
        modcache : dict = gzdr.load_modcache()
        
        self.iwad = values[IWAD_NAME]

        if self.iwad in bignames:
            self.iwad += ".WAD"
        
        elif self.iwad in STEAM_NAMES.keys():
            self.iwad = STEAM_NAMES[self.iwad]

        modcache["exec"]["iwad"] = self.iwad
        gzdr.custom.save_modcache(modcache)

    
    def update_iwad(self, event: any, values: any):
        bignames : list = ["DOOM", "DOOM2", "HEXEN", "PLUTONIA", "TNT"]
        modcache : dict = gzdr.load_modcache()

        self.iwad = values[IWAD_LIST][0]
        
        if self.iwad in bignames:
            self.iwad += ".WAD"
        
        elif self.iwad in STEAM_NAMES.keys():
            self.iwad = STEAM_NAMES[self.iwad]
        
        if self.iwad.endswith(".WAD"):
            self.window[IWAD_NAME].update(self.iwad[:-4])
        
        else:
            self.window[IWAD_NAME].update(self.iwad)

        modcache["exec"]["iwad"] = self.iwad
        gzdr.custom.save_modcache(modcache)
    
    def set_warp_map(self, event: any, values: any):
        modcache : dict = gzdr.load_modcache()
        self.warp_map = values[WARP_MAP].upper()
        self.window[WARP_MAP].update(self.warp_map)
        modcache["exec"]["warp"] = self.iwad
        gzdr.custom.save_modcache(modcache)
    
    def set_difficulty(self, event: any, values: any):
        modcache : dict = gzdr.load_modcache()
        self.difficulty = values[DIFFICULTY]
        self.window[DIFFICULTY].update(self.difficulty)
        modcache["exec"]["skill"] = self.iwad
        gzdr.custom.save_modcache(modcache)
    

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
    modcache   : dict = gzdr.load_modcache()
    title      : str  = f"GZDoom Run v{gzdr.VERSION_MAJOR}.{gzdr.VERSION_MINOR}.{gzdr.VERSION_PATCH}"
    iwad_listln: int  = len(iwad_list)
    iwad_name  : str  = modcache["exec"]["iwad"]

    if modcache["first?"]:
        modcache["first?"] = False 
        modcache["path"]["iwad"] = DEFAULT_PATH
        
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
            gui.In(modcache["path"]["iwad"], text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, size=(23, 1), enable_events=True, key=DIRECTORY),
            gui.FolderBrowse(button_color=BUTTON_COLOR)
        ],
        [gui.Listbox(mod_list, enable_events=True, text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, sbar_trough_color=CLICK_BACKGROUND, sbar_arrow_color=CLICK_BACKGROUND, sbar_background_color=BACKGROUND, size=(38, 8), key=MOD_LIST)]
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
            [gui.Frame("dmflags", background_color=BACKGROUND, p=3, layout=[[gui.In(str(modcache["exec"]["dmflags"]), size=(39, 1), text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, enable_events=True, key=SET_DMFLAGS)]])],
            [gui.Frame("dmflags2", background_color=BACKGROUND, p=3, layout=[[gui.In(str(modcache["exec"]["dmflags2"]), size=(39, 1), text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, enable_events=True, key=SET_DMFLAGS2)]])]
    ]

    if iwad_listln > 0:
        if iwad_listln <= 8:
            iwad_block.append([gui.Listbox(iwad_list, text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, sbar_trough_color=CLICK_BACKGROUND, sbar_arrow_color=CLICK_BACKGROUND, sbar_background_color=BACKGROUND, enable_events=True, size=(38, iwad_listln), key=IWAD_LIST)])

        else:
            iwad_block.append([gui.Listbox(iwad_list, text_color=TEXT_COLOR, background_color=INPUT_BACKGROUND, sbar_trough_color=CLICK_BACKGROUND, sbar_arrow_color=CLICK_BACKGROUND, sbar_background_color=BACKGROUND, enable_events=True, size=(38, 8), key=IWAD_LIST)])

    return Application(title, iwad_block, pwad_block, launch_pad, dmflags_layout, modcache)

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
    options : CommandOptions = CommandOptions(gzdr.custom.load_directory())
    
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

# '''
# Main Block
# '''
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        sys.exit(run_from_cli(len(sys.argv), sys.argv))
        
    else:
        run_with_gui()
