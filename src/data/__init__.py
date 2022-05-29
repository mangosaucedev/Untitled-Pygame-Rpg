import os

from typing import List

TEXTURES_PATH = os.path.abspath(os.path.join(os.pardir, "assets", "textures"))

def scan_dir(path: str) -> List[os.DirEntry]:
    return os.scandir(path)