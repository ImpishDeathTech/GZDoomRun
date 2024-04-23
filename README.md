# GZDoom Run
## Version 1.4
### A small tool for loading GZDoom mods on Linux a little easier. 
> This a persosnal program that was originally just a simple python sciript meant to used with Steam to help me load doom mods easier, 
> but has evolved into a full blown Doom Loader that has a few command line options that make it a fine personal program.
> Type `gzdrun help all` once installed to see these options.
> Requires python3 and PySimpleGUI to be installed on your sistem.
> This program is really for my own usage, this help is just here as a reference for myself,
> you can use it yourself, but the application's development is currently paused due to the recent decisions of the PySimpleGUI API to require proprietary licensing.
> This was supposed to be a **__free__** application, and may stay that way, so I may or may not pay for this license, but I may just rewrite the entire app all together. 
> The application automatically searches the steam directory, if present, for any IWADs, and the .config/gzdoom directory for any PWADs or PK3s.

## GZDoom Run Python GUI - Seems we've gotta redo EVERYTHING! You can still play with it though! ^,..,^
![Alt text](https://github.com/ImpishDeathTech/GZDoomRun/blob/master/Screenshot.jpg)
> The gui is currently written in python with PySimpleGUI, which has recently gone proprietary, and implemented an all-consuming license which stunts my ability to release this as a free software application
> in it's current state. As of this moment, this program is for personal use only (mostly my own), so you'll have to head [here](https://pysimplegui.com/pricing) and grab a free developers license so you can get a developer
> key if you want to run this Doom Loader and fiddle with it's code (I won't be developing the python side any further myself, if that changes for any reason whatsoever, you will see the changes here) until I can rebuild in C++
> or a more solid, efficient language than python such as it. The resulting application will remain free software.
> This application, under all intensive purposes,is for fun, It's a Doom Loader. It was born of tinkering and made to be tinkered with. To build on, to grow. One of my goals with all of my applications is to make them extendable
> and customizable in some way. I will leave the python branch as an educational and personal reference. 


## Tutorial

### Installation 
> First, make sure you have GZDoom installed natively, no snap or flatpak crap.
> Then, download most recent the Release [Zip](https://github.com/ImpishDeathTech/GZDoomRun/releases/download/gzdoom-v1-4-0-0/GZDoomRun_v1.4.0-0.zip) version and unload it:
```sh
unzip GZDoomRunL_vX.X.X-X.zip
```
> Next, cd into the project directory and execute the install.sh script.
```sh
cd GZDoomRun
# you'll want to make a .venv if you haven't already, like so.
make .venv && make install
```
> The above will create a python virtual environment named in /home/username/.venv directory, otherwise, create one by typing
```sh
python3 -m venv /path/to/venv && python3 -m venv /path/to/.venv/bin/activate
make install
```
> You will have to edit the `VENV` var in gzdrun.sh with /path/to/.venv

> If you want to install it to the native environment (Not Reccomended!!!), of course, you could always type the following:
```sh
make install-system
```
> But I'd advise otherwise. Best practice is to use a .venv

### Running
> Now, we'll test it by extracting the provided pkz and installing Brutal Doom! The following options will only be usable if you have SIGIL and Brutal Doom installed to your .config/gzdoom directory.
> You'll always want to make sure you have your python virtual environment running. 
```sh
gzdrun install SIGIL_v1_21.pkz
gzdrun iwad DOOM.WAD warp E1M1 skill 4 with SIGIL_v1_21

# Loading multiple wads is done by seperating each wad name by a '%'
gzdrun iwad DOOM.WAD with SIGIL_v1_21%SIGIL_v1_21_COMPAT%brutalv21

# It is also possible to warp to a specific map, and choose a difficulty
gzdrun iwad DOOM.WAD warp E1M1 skill 4 with SIGIL_v1_21
```
gzdoomrun will launch as a gui application if no arguments are provided. When you select an IWAD from the list, it's key will appear in the "Path" input, which represents it's file stem. This input accepts these known file stems, as well as full paths, in case your IWAD is not a IWAD that I personally use or own.

For the PWADs, either select the key or type it in. The list will automatically update based on what is contained within the input box. "Browse" buttons are provided alongside both of these inputs, so that you may browse your drive for either path.

## DMFlags
The DMFlags section accepts the following constants and their related values. Note that these constants do not work at command-line level, and are strictly GUI related, you should likely use the decimal equivilant to the
related hexadecimal values provided:

| DMFlag                          | Value     | DMFlag 2                        | Value     |
|---------------------------------|-----------|---------------------------------|-----------|
| ALLOW_HEALTH                    | $1        | DROP_WEAPON                     | $2        |
| ALLOW_POWERUPS                  | $2        | NO_TEAM_CHANGING                | $10       |
| WEAPONS_STAY                    | $4        | DOUBLE_AMMO                     | $40       |
| FALL_DMG                        | $8        | DEGENERATION_ON                 | $80       |
| FALL_DMG_HEXEN                  | $10       | ALLOW_BFG_AIMING                | $100      |
| FALL_DMG_STRIFE                 | $18       | BARRELS_RESPAWN                 | $200      |
| SAME_MAP                        | $40       | RESPAWN_PROTECTION              | $400      |
| SPAWN_FARTHEST                  | $80       | SPAWN_WHERE_DIED                | $1000     |
| FORCE_RESPAWN                   | $100      | KEEP_FRAGS_GAINED               | $2000     |
| ALLOW_ARMOR                     | $200      | NO_RESPAWN                      | $4000     |
| ALLOW_EXIT                      | $400      | LOSE_FRAG_ON_DEATH              | $8000     |
| INFINITE_AMMO                   | $800      | INFINITE_INVENTORY              | $10000    |
| NO_MONSTERS                     | $1000     | NO_MONSTERS_TO_EXIT             | $20000    |
| MONSTERS_RESPAWN                | $2000     | ALLOW_AUTOMAP                   | $40000    |
| ITEMS_RESPAWN                   | $4000     | AUTOMAP_ALLIES                  | $80000    |
| FAST_MONSTERS                   | $8000     | ALLOW_SPYING                    | $100000   |
| ALLOW_JUMP                      | $10000    | CHASECAM_CHEAT                  | $200000   |
| ALLOW_FREELOOK_OFF              | $40000    | DISALLOW_SUICIDE                | $400000   |
| ALLOW_FREELOOK                  | $80000    | ALLOW_AUTOAIM                   | $800000   |
| ALLOW_FOV                       | $100000   | CHECK_AMMO_FOR_WEAPON_SWITCH    | $1000000  |
| SPAWN_MULTI_WEAPONS             | $200000   | ICON_OF_SINS_DEATH_KILLS_SPAWNS | $2000000  |
| ALLOW_CROUCH                    | $400000   | END_SECTOR_COUNTS_FOR_KILLS     | $4000000  |
| LOOSE_INVENTORY                 | $1000000  | BIG_POWERUPS_RESPAWN            | $8000000  |
| KEEP_KEYS                       | $2000000  | ALLOW_VERTICAL_BULLET_SPREAD    | $40000000 |
| KEEP_WEAPONS                    | $4000000  | DMFLAGS2_DEFAULT                | $79C0100  |
| KEEP_ARMOR                      | $8000000  |
| KEEP_POWERUPS                   | $10000000 |
| KEEP_AMMO                       | $20000000 |
| LOSE_HALF_AMMO                  | $40000000 |
| DMFLAGS_DEFAULT                 | $3E750603 |

The input accepts multiple parameters, and the program automatically caps-locks this input section, and converts - to _ so you have to press shift less. 
The same goes for the map choice input, which accepts the "E1M1" or "MAP01" formats. Relational constants for the difficulty level per-game could be implemented
in the future.

All GZDRun settings are saved to the modcache.json, under "exec", locaded in .config/gzdoom.

I'll make a video soon


### Uninstall
simply run `make uninstall` 
