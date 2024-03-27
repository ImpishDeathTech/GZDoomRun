# GZDoom Run
### A small tool for loading GZDoom mods on Linux a little easier. 

> This program was originally meant to used with Steam to help me load doom mods easier, 
> but has a few command line options that make it a fine standalone program.
> Type `gzdoomrun help` once installed to see these options.
> Requires python3 and PySimpleGUI to be installed on your sistem, racket for v1.3.1

## GZDoom Run GUI
> The gui is currently written in racket, may be rewritten in C with SDL2, or C++ with SFML, more likely the latter 

## Tutorial

### Installation 
> First, make sure you have GZDoom installed natively, no snap or flatpak crap.
 > Then, download most recent the Release [Zip](https://github.com/ImpishDeathTech/GZDoomRun/releases/download/gzdoom-v1-3-2-1/GZDoomRun_SIGIL_v1.3.2-1.zip) or [Tarball](https://github.com/ImpishDeathTech/GZDoomRun/releases/download/gzdoom-v1-3-2-1/GZDoomRun_SIGIL_v1.3.2-1.tar.gz) version and unload it:
```sh
unzip GZDoomRun_SIGIL_vX.X.X-X.zip
# or
tar -xvf GZDoomRun_SIGIL_vX.X.X-X.tar.gz
```
> Next, cd into the project directory and execute the install.sh script.
```sh
cd GZDoomRun
./install gzdoom
```

### Running
> Now, we'll test it by extracting the provided tarball and installing Brutal Doom! The following options will only be usable if you download one of the GZDoomRun_BRUTAL or GZDoomRun_SIGIL builds.
> This will also create a desktop shortcut for loading Brutal Doom and SIGIL.
```sh
./install brutal
./install sigil
gzdoomrun with brutalv21

# Loading multiple wads is done by seperating each wad name by a '%'
gzdoomrun with SIGIL_v1_21%SIGIL_v1_21_COMPAT%brutalv21
```
gzdoomrun will launch gzdoom on it's own if no arguments are provided

And that's it! Now, Setting it up with steam is pretty easy.
Go to your Library, and click Add Game at the bottom. A list of your applications should pop up and we can add GZDoom from there.
Then, once added, we right click the "game" in our library, go to Properties in the menu, (the little gear button on it's library page), and under the Shortcut properties, we change the TARGET from "gzdoom" to "gzdoom-run"
Then, in LAUNCH OPTIONS under the same tab, we can add our mod keywords easily.

I'll make a video soon


### Uninstall
simply run the uninstall script as you did the install, and you should be golden.
