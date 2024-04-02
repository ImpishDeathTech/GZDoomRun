# a custom help file
# change name to help.py to overwrite old help function

import sys, os, json

from pathlib import Path

MODCACHE_PATH    : str   = os.path.join(Path.home(), ".config", "gzdoom", "modcache.json")

def load_modcache() -> dict:
    with open(MODCACHE_PATH, "r") as f:
        data = json.load(f)
        return dict(data)

modcache : dict = load_modcache()

HELP_STRING       : str = F"""
    GZDoom Run v{modcache["version"][0]}.{modcache["version"][1]}.{modcache["version"][2]} Help
        
        GZDoom Run is a small linux program for loading GZDoom mods
        a little easier. This program is meant to be used with Steam 
        but can be used in standalone, and has a few command line options:
"""

HELP_VARS  : dict = {
    "help":  ("help [sym]", "       Prints a help message. type a command name alongside to get detailed description"),
    "iwad": ("iwad [IWAD Name/Path]", 
    '''
            If the (case sensitive) name provided exists as a known IWAD to GZDoom,
            the engine will boot it with any subsequent arguments. Must come first in
            a list of command line parameters.
    '''),
    "warp": ("warp E[n]M[n] / MAP[n][n]",
'''
            For Doom II, Final Doom, Hexen and Strife, starts the game on map m. 
            For Chex Quest, Doom and Heretic, starts the game on episode e, map m. 
            The +map command can also be used to perform this action, but it expects 
            the actual name of the map (e.g. MAP01, E1M1). must come after 'iwad', 
            and before 'skill' and 'with'.
'''),
        
    "skill": ("skill 'Difficulty Name'",
'''
            Sets the difficulty name for the warped-to map provided. (eg skill "Ultraviolence")
            Must be provided afer 'iwad' and 'warp', and before 'with'
'''),

    "with": ("with [PWAD Names]",
'''   
            Searches the mod directory for any WADs or PK3s resembling the
            provided keyword. This search is case sensitive, and is the default operation
            when no option keyword is provided. Otherwise, must come after 'iwad', 'warp' 
            and 'skill' consecutively
'''),
    "install"  : ("install [file names]", "If they exist, installs the provided WAD, PKZ and PK3 files to GZdoom"),
    "uninstall": ("remove [keywords]", "If they exist, uninstalls the related WAD and PK3 files (testing)"),
    "makepkz"  : ("makepkz [directory]", "Creates a .pkz archive from a directory")
}

del modcache

def main(argc: int, argv: list):
    if argv[0] == "all" or argv[0] == "list":
        print(HELP_STRING)
        print("   Command List:\n")
        for key in HELP_VARS.keys():
            print(f"\t{key}")

        print("\nRun 'gzdoom help [command name]' for more information")

    elif argv[0] in HELP_VARS.keys():
        print(HELP_STRING)
        print(F'''   {HELP_VARS[argv[0]][0]}

        {HELP_VARS[argv[0]][1]}
        ''')
    else:
        print(HELP_STRING)
        print('''
    Type gzdoomrun help list for a list of commands, and gzdoom help [command name] for details on that command
        ''')

    sys.exit(0)