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


DIRECTORY   : str = "@ directory path"
MOD_LIST    : str = "@ WAD/PK3 list"
IWAD_NAME   : str = "@ IWAD name"
IWAD_LIST   : str = "@ IWAD list"
RUN_ARGS    : str = "@ run arguments"
ARTWORK     : str = "@ game artwork"
EXECUTE     : str = "@ run gzdoom"
CLEAR_ARGS  : str = "@ clear arguments"
EXIT_APP    : str = "@ exit application"


# Paths
DEFAULT_PATH: str = os.path.join(Path.home(), ".config", "gzdoom")
STEAM_PATH  : str = os.path.join(Path.home(), ".local", "share", "Steam", "steamapps", "common")

STEAM_NAMES : dict = {
    "The Ultimate Doom": "DOOM.WAD",
    "Doom 2": "DOOM2.WAD",
    "Final Doom: The Plutonia Experiment": "PLUTONIA.WAD",
    "Final Doom: TNT Evilution": "TNT.WAD",
    "Doom (Shareware)": "doom1",
    "Doom (Unity)": "doom",
    "Doom 2 (Unity)": "doom2",
    "Hexen: Beyond Heretic": "HEXEN.WAD"
}



class Application:

    def __init__(self, title: str, iwad_table: list, pwad_table: list, launch_pad: list):
        self.title      : str                 = title
        self.is_running : bool                = True
        self.options    : gzdr.CommandOptions = gzdr.CommandOptions([])
        self.run_args   : str                 = ""
        self.iwad       : str                 = ""

        self.events : dict = {
            DIRECTORY : self.list_directory,
            MOD_LIST  : self.update_run_args,
            IWAD_LIST : self.update_iwad,
            IWAD_NAME : self.set_iwad,
            RUN_ARGS  : self.update_arglist,
            EXECUTE   : self.run_gzdoom,
            CLEAR_ARGS: self.clear_arguments,
            EXIT_APP  : self.exit_application
        }

        self.layout : list = [
            [gui.Column(iwad_table)],
            [gui.Column(pwad_table)],
            [gui.Column(launch_pad)]
        ]

        self.window       : gui.Window = gui.Window(title=self.title, layout=self.layout)
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
            print(self.run_args)
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
                self.options.process_arguments(4, ["iwad", self.iwad, "with", self.run_args])
                
            else:
                self.options.process_arguments(2, ["iwad", self.iwad])
                
        
        except gzdr.GZDoomRunError as e:
            print(e.what(False))
        

    def clear_arguments(self, event: any, values: any):
        self.window[RUN_ARGS].update("")
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
    

    def run(self):
        while self.is_running:
            e, v = self.window.read()

            if e == gui.WIN_CLOSED:
                break

            elif self.find(e):
                self.execute(e, v)

        self.window.close()

        

def make_application(mod_list: list, iwad_list: list) -> Application:
    title      : str  = f"GZDoom Run v{gzdr.VERSION_MAJOR}.{gzdr.VERSION_MINOR}.{gzdr.VERSION_PATCH}"
    iwad_listln: int  = len(iwad_list)

    iwad_block : list = [
        [
            gui.Text("Run IWAD"),
            gui.In(size=(25, 1), enable_events=True, key=IWAD_NAME),
            gui.FolderBrowse()
        ]
    ]

    pwad_block : list = [
        [
            gui.Text("Mod Folder"),
            gui.In(DEFAULT_PATH, size=(25, 1), enable_events=True, key=DIRECTORY),
            gui.FolderBrowse()
        ],
        [gui.Listbox(mod_list, enable_events=True, size=(45, 8), key=MOD_LIST)]
    ]

    launch_pad : list = [
        [
            gui.Text("Launch With"),
            gui.In(size=(34, 1), enable_events=True, key=RUN_ARGS)
        ],
        [
            gui.Button("Run", enable_events=True, key=EXECUTE),
            gui.Button("Clear", enable_events=True, key=CLEAR_ARGS),
            gui.Button("Exit", enable_events=True, key=EXIT_APP)
        ]
    ]

    if iwad_listln > 0:
        if iwad_listln <= 8:
            iwad_block.append([gui.Listbox(iwad_list, enable_events=True, size=(45, iwad_listln), key=IWAD_LIST)])

        else:
            iwad_block.append([gui.Listbox(iwad_list, enable_events=True, size=(45, 8), key=IWAD_LIST)])
    
    return Application(title, iwad_block, pwad_block, launch_pad)


# This will list IWADS from Steam based on those I personally own
def load_iwads(folder_list: list) -> list:
    iwad_names : list = []
    keys       = list(STEAM_NAMES.keys())

    for folder in folder_list:
        if folder == "Ultimate Doom":
            iwad_names.append(keys[0])
        
        elif folder == "Doom 2":
            iwad_names += [keys[1], keys[2], keys[3]]
        
        elif folder == "Hexen":
            iwad_names.append(keys[7])
    
    if (keys[0]) in iwad_names:
        iwad_names += [keys[4], keys[5]]
    
    if (keys[1]) in iwad_names:
        iwad_names.append(keys[6])

    return iwad_names


'''
# This function will list PWADS and PK3s in the directory DEFAULT_PATH.
# This path can be changed dynamically by simply typing into
# the 'Mod Folder' input
'''
def load_pwads(file_list: list) -> list:
    file_names : list = []

    for file_name in file_list:
        if os.path.isfile(os.path.join(DEFAULT_PATH, file_name)) and file_name.lower().endswith(gzdr.custom.WAD_SUFFIXES):
            file_names.sort(key=str.lower)
            file_names.append(file_name[:-4])
    
    return file_names


# this will run the application from command line
def run_from_cli(argc: int, argv: list) -> int:
    options : gzdr.CommandOptions = gzdr.CommandOptions(gzdr.custom.load_directory())
    
    try:
        argv.pop(0)
        options.process_arguments(argc - 1, argv)
    
    except gzdr.GZDoomRunError as e:
        e.what()
        return 1
    
    return 0


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
