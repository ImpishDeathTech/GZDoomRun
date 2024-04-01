#! /usr/bin/python3

import importlib.util, sys, os
import PySimpleGUI as gui 
import gzdoomrunlib as gzdr

from types import ModuleType
from importlib.machinery import ModuleSpec
from pathlib import Path

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


class Application:

    def __init__(self, title: str, iwad_table: list, pwad_table: list, argument_input: list):
        self.title      : str                 = title
        self.is_running : bool                = True
        self.options    : gzdr.CommandOptions = gzdr.CommandOptions([])
        self.run_args   : str                 = ""
        self.iwad       : str                 = "doom1"

        self.events : dict = {
            DIRECTORY : self.list_directory,
            MOD_LIST  : self.update_image_and_args,
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
            [gui.Column(argument_input)]
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


    def update_image_and_args(self, event: any, values: any):
        try:
            file_name = os.path.join(values[DIRECTORY], values[MOD_LIST][0])
            run_args = values[RUN_ARGS].split(" ")
            run_args.append(values[MOD_LIST][0])
            self.run_args = "%".join(run_args)
            self.window[RUN_ARGS].update(" ".join(run_args))

        except:
            pass

    
    def update_arglist(self, event: any, values: any):
        if self.run_args != "":
            self.run_args += "%"
            self.run_args += "%".join(values[RUN_ARGS].split(" "))
        
        else:
            self.run_args += "%".join(values[RUN_ARGS].split(" "))


    def run_gzdoom(self, event: any, values: any):
        try:
            if (self.iwad != "doom1") and self.run_args:
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

    
    def update_iwad(self, event: any, values: any):
        bignames : list = ["DOOM", "DOOM2", "HEXEN", "PLUTONIA", "TNT"]
        self.iwad = values[IWAD_LIST][0]
        self.window[IWAD_NAME].update(self.iwad)
        
        if self.iwad in bignames:
            self.iwad += ".WAD"
        
        elif self.iwad.endswith("(Unity)"):
            self.iwad = self.iwad[:-len(" (Unity)")].lower()
        
        elif self.iwad.endswith("(Shareware)"):
            self.iwad = "doom1"

        

def make_application(mod_list: list, iwad_list: list) -> Application:
    return Application(f"GZDoom Run v{gzdr.VERSION_MAJOR}.{gzdr.VERSION_MINOR}.{gzdr.VERSION_PATCH}",
    [
        [
            gui.Text("Run IWAD"),
            gui.In("DOOM (Shareware)", size=(25, 1), enable_events=True, key=IWAD_NAME),
            gui.FolderBrowse()
        ],
        [gui.Listbox(iwad_list, enable_events=True, size=(45, 10), key=IWAD_LIST)]
    ],
    [
        [
            gui.Text("Mod Folder"),
            gui.In(DEFAULT_PATH, size=(25, 1), enable_events=True, key=DIRECTORY),
            gui.FolderBrowse()
        ],
        [gui.Listbox(mod_list, enable_events=True, size=(45, 10), key=MOD_LIST)]
    ],
    [
        [
            gui.Text("Launch With"),
            gui.In(size=(34, 1), enable_events=True, key=RUN_ARGS)
        ],
        [
            gui.Button("Run", enable_events=True, key=EXECUTE),
            gui.Button("Clear", enable_events=True, key=CLEAR_ARGS),
            gui.Button("Exit", enable_events=True, key=EXIT_APP)
        ]
    ])


def run_gui():
    file_names   : list = []
    iwad_names   : list = []

    try:
        file_list : list = os.listdir(DEFAULT_PATH)
    except:
        file_list : list = []
    finally:
        for file_name in file_list:
            if os.path.isfile(os.path.join(DEFAULT_PATH, file_name)) and file_name.lower().endswith(gzdr.custom.WAD_SUFFIXES):
                file_names.sort(key=str.lower)
                file_names.append(file_name[:-4])
    
    try: 
        folder_list : list = os.listdir(STEAM_PATH)
    except:
        folder_list : list = []
    finally:
        extras : list = []

        for folder in folder_list:
            if folder == "Ultimate Doom":
                iwad_names.append("DOOM")
            
            elif folder == "Doom 2":
                iwad_names += ["DOOM2", "PLUTONIA", "TNT"]
            
            elif folder == "Hexen":
                iwad_names.append("HEXEN")
        
        if "DOOM" in iwad_names:
            iwad_names += ["DOOM (Shareware)", "DOOM (Unity)"]
        
        if "DOOM2" in iwad_names:
            iwad_names.append("DOOM2 (Unity)")
        
        iwad_names += extras

    app : Application = make_application(file_names, iwad_names + extras)

    while app.is_running:
        e, v = app.window.read()

        if e == gui.WIN_CLOSED:
            break

        elif app.find(e):
            app.execute(e, v)

    app.window.close()


def run_cli(argc: int, argv: list):
    options : gzdr.CommandOptions = gzdr.CommandOptions(gzdr.custom.load_directory())
    
    try:
        sys.argv.pop(0)
        options.process_arguments(argc - 1, sys.argv)
        sys.exit(0)
    
    except gzdr.GZDoomRunError as e:
        e.what()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        run_cli(len(sys.argv), sys.argv)
        
    else:
        run_gui()
