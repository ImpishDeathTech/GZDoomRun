import os, json

from pathlib import Path
from zipfile import ZipFile

WAD_DIRECTORY  : str  = os.path.join(Path.home(), ".config", "gzdoom")
WAD_SUFFIXES   : list = (".wad", "pk3")
GZDOOM_INSTALL : str  = "[GZDoom Run Install]: "
MODCACHE_PATH  : str  = os.path.join(WAD_DIRECTORY, "modcache.json"),

def load_modcache() -> dict:
    with open(MODCACHE_PATH, "r") as f:
        data = json.load(f)
        return dict(data)


def save_modcache(data: dict):
    with open(MODCACHE_PATH, "w") as f:
        f.truncate()
        json.dump(data, f)


def save_manifest(name: str, manifest: list):
    cache : dict = load_modcache()
    cache["manifest"][name] = manifest
    save_modcache(cache)


def install_packet_archive(file_name: str):
    manifest : list = []
    outpath  : str  = os.path.join(WAD_DIRECTORY, file_name)

    print(GZDOOM_INSTALL + f" {file_name} to {outpath} ...")
    
    with ZipFile(file_name, mode='r', allowZip64=True) as zip_file:
        for name in zip_file.namelist():
            if name.endswith(WAD_SUFFIXES):
                manifest.append(name)
                zip_file.extract(name, path=outpath)
    
    save_manifest(file_name[:-4], manifest)

    print(GZDOOM_INSTALL + f"{file_name} installed to {outpath} successfully")


def install_packet_file(file_name: str):
    modcache : dict = load_modcache()
    outpath  : str  = os.path.join(WAD_DIRECTORY, file_name)

    print(f"{GZDOOM_INSTALL} {file_name} to {outpath} ...")

    result : CompletedProcess = subprocess.run(["cp", file_name, outpath])

    if result.returncode != 0:
        raise GZDoomRunError(result.returncode, result.stderr)
    
    else:
        modcache["default"]["manifest"].append(file_name)

    save_modcache(modcache)
    print(f"{GZDOOM_INSTALL} {file_name} installed to {outpath} successfully")
	

# gzdoom-run install [file names]
def main(argc: int, argv: list):
    for file_name in argv:
        if file_name.endswith(".pkz"):
            install_packet_archive(file_name)

        elif file_name.endswith(WAD_SUFFIXES):
            install_packet_file(file_name)

    sys.exit(0)