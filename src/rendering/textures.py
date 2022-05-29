import data
import pygame

from typing import Dict, Optional

TEXTURE_LIBRARY: Dict[str, pygame.Surface] = dict()

def get(texture_name: str) -> pygame.Surface:
    
    if not TEXTURE_LIBRARY.get(texture_name, None):
        texture = __load(data.TEXTURES_PATH, texture_name)
        
        if not texture:
            raise Exception(f"No texture named {texture_name} can be found in {data.TEXTURES_PATH}")
        
        TEXTURE_LIBRARY[texture_name] = texture
    return TEXTURE_LIBRARY[texture_name]
        
def __load(rootdir: str, texture_name: str) -> Optional[pygame.Surface]:
    import os
    
    for item in os.scandir(rootdir):
        if os.path.isfile(item) and item.name == texture_name:
            return pygame.image.load(item)
    for item in os.scandir(rootdir):
        if item.is_dir():
            texture = __load(item, texture_name)
            if texture:
                return texture
    return None
    