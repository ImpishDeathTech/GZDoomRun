#! /usr/bin/python3

import importlib.util, sys, os
import PySimpleGUI as gui 
import gzdoomrun as gzdr

from types import ModuleType
from importlib.machinery import ModuleSpec


DIRECTORY  : str = "@directory_path"
FILES      : str = "@file_list"
RUN_ARGS   : str = "@run_arguments"
ARTWORK    : str = "@game_artwork"
EXECUTE    : str = "$run_gzdoom"
CLEAR_ARGS : str = "$clear_arguments"
EXIT_APP   : str = "$exit_application"

class Application:

    def __init__(self, title: str, file_table: list, argument_input: list):
        self.title      : str                 = title
        self.is_running : bool                = True
        self.options    : gzdr.CommandOptions = gzdr.CommandOptions([])
        self.run_args   : str                 = ""
        
        self.events : dict = {
            DIRECTORY : self.list_directory,
            FILES     : self.update_image_and_args,
            RUN_ARGS  : self.update_arglist,
            EXECUTE   : self.run_gzdoom,
            CLEAR_ARGS: self.clear_arguments,
            EXIT_APP  : self.exit_application
        }

        self.layout : list = [
            [gui.Column(file_table)],
            [gui.Column(argument_input)]
        ]

        self.window : gui.Window = gui.Window(title=self.title, layout=self.layout)
    
    def find(self, event: any):
        for key in self.events.keys():
            if key == str(event):
                return True
        
        return False
    
    
    def execute(self, event: any, values: any):
        self.events[str(event)](event, values)


    def list_directory(self, event: any, values: any):
        folder = values[DIRECTORY]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        finally:
            file_names = []

            for file_name in file_list:
                if os.path.isfile(os.path.join(folder, file_name)) and file_name.lower().endswith(gzdr.custom.WAD_SUFFIXES):
                    file_names.append(file_name[:-4])

            self.window[FILES].update(file_names)


    def update_image_and_args(self, event: any, values: any):
        try:
            file_name = os.path.join(values[DIRECTORY], values[FILES][0])
            run_args = values[RUN_ARGS].split(" ")
            run_args.append(values[FILES][0])
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
            self.options.process_arguments(2, ["with", self.run_args])
        
        except gzdr.GZDoomRunError as e:
            print(e.what(False))
        

    def clear_arguments(self, event: any, values: any):
        self.window[RUN_ARGS].update("")
        self.run_args = ""


    def exit_application(self, event: any, values: any):
        self.is_running = False


if __name__ == "__main__":
    app : Application = Application(f"GZDoom Run v{gzdr.VERSION_MAJOR}.{gzdr.VERSION_MINOR}.{gzdr.VERSION_PATCH}",
    [
        [
            gui.Text("Mod Folder"),
            gui.In(size=(25, 1), enable_events=True, key=DIRECTORY),
            gui.FolderBrowse()
        ],
        [gui.Listbox(values=[], enable_events=True, size=(49, 20), key=FILES)]
    ],
    [
        [
            gui.Text("Launch With"),
            gui.In(size=(25, 1), enable_events=True, key=RUN_ARGS)
        ],
        [
            gui.Button("Run", enable_events=True, key=EXECUTE),
            gui.Button("Clear", enable_events=True, key=CLEAR_ARGS),
            gui.Button("Exit", enable_events=True, key=EXIT_APP)
        ]
    ])

    while app.is_running:
        e, v = app.window.read()

        if e == gui.WIN_CLOSED:
            break

        elif app.find(e):
            app.execute(e, v)

    app.window.close()