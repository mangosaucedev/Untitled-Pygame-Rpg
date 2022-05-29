import pygame 
import rendering
import rendering.textures

from typing import List, Tuple

class Tile(rendering.RenderObject):
    
    def __init__(self, position: Tuple[int, int], image: pygame.Surface = pygame.Surface([1, 1])):
        self.position = position
        rendering.RenderObject.__init__(self, image, rendering.RenderOrder.TILES)
        all_tiles.append(self)
    
    @property    
    def position(self) -> Tuple[int, int]:
        return self.__position
        
    @position.setter
    def position(self, position: Tuple[int, int]):
        self.__position = position
    
all_tiles: List[Tile] = list()
    
def create_tile(position: Tuple[int, int], texture_name: str) -> Tile:
    return Tile(position, rendering.textures.get(texture_name))

def clear_tiles():
    while all_tiles.__len__() > 0:
        tile = all_tiles.pop()
        tile.kill()