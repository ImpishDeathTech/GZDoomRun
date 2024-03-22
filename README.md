# GZDoom Run
### A small tool for loading GZDoom mods on Linux a little easier. 

> This program was originally meant to used with Steam to help me load doom mods easier, 
> but has a few command line options that make it a fine standalone program.
> Type `gzdoom-run help` once installed to see these options.

## GZDoom Run GUI
> The gui is currently written in racket, may be rewritten in C with SDL2, C++ with SFML, more likely the latter 

## Tutorial

### Installation 
> First, make sure you have GZDoom installed natively, no snap or flatpak crap. Then, download the git repo:
```sh
git clone https://github.com/ImpishDeathTech/GZDoomRun.git
```
 > or download the Release [Zip](https://github.com/ImpishDeathTech/GZDoomRun/releases/download/gzdoom-run-v1-3-1/GZDoomRun_v1.3.1_BRUTAL.zip) or [Tarball](https://github.com/ImpishDeathTech/GZDoomRun/releases/download/gzdoom-run-v1-3-1/GZDoomRun_v1.3.1_BRUTAL.tar.gz) version and unload it:
```sh
unzip GZDoomRun_vX.X.X_BRUTAL.zip
# or
tar -xvf GZDoomRun_vX.X.X_BRUTAL.tar.gz
```
> Next, cd into the project directory and execute the install.sh script.
```sh
cd GZDoomRun
./install gzdoom
```

### Running
> Now, we'll test it by extracting the provided tarball and installing Brutal Doom! this will only be available if you download one of the GZDoomRun_vX.X.X_BRUTAL builds
> This will also create a desktop shortcut for loading Brutal Doom
./install brutal
gzdoom-run brutalv21
```
gzdoom-run will launch gzdoom on it's own if no arguments are provided

And that's it! Now, Setting it up with steam is pretty easy.
Go to your Library, and click Add Game at the bottom. A list of your applications should pop up and we can add GZDoom from there.
Then, once added, we right click the "game" in our library, go to Properties in the menu, (the little gear button on it's library page), and under the Shortcut properties, we change the TARGET from "gzdoom" to "gzdoom-run"
Then, in LAUNCH OPTIONS under the same tab, we can add our mod keywords easily.

I'll make a video soon


### Uninstall
simply run the uninstall script as you did the install, and you should be golden.
