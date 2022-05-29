import pygame

from typing import Tuple

class Camera():
    
    def __init__(self):
        super().__init__()

        self.__position: Tuple[int, int] = (0, 0)
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        self.width, self.height = self.display_surface.get_size()
        self.frustrum: pygame.Rect =  pygame.Rect(0, 0, self.width, self.height)
        
    @property
    def position(self) -> Tuple[int, int]:
        return self.__position
     
    @position.setter
    def position(self, position: Tuple[int, int]):
        self.__position = position
        x, y = position
        self.frustrum.x = x
        self.frustrum.y = y 
     
    def move(self, direction: Tuple[int, int]):
        ox, oy = self.position
        dx, dy = direction
        self.position = (ox + dx, oy + dy)
        
MAIN = Camera()

