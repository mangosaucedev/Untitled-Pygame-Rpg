import pygame

from events import Event
from typing import Tuple

class Camera():
    
    def __init__(self):
        self.__position: Tuple[int, int] = (0, 0)
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        self.width, self.height = self.display_surface.get_size()
        self.frustrum: pygame.Rect =  pygame.Rect(0, 0, self.width, self.height)
        self.on_camera_position_changed: Event = Event()
        
    @property
    def position(self) -> Tuple[int, int]:
        return self.__position
     
    @position.setter
    def position(self, position: Tuple[int, int]):
        self.__position = position
        x, y = position
        self.frustrum.x = x
        self.frustrum.y = y 
        self.on_camera_position_changed(self.position)
     
    def move(self, direction: Tuple[int, int]):
        ox, oy = self.position
        dx, dy = direction
        self.position = (ox + dx, oy + dy)
    
    def is_within_frustrum(self, rect: pygame.Rect) -> bool:
        return rect.colliderect(self.frustrum)
    
    def zoom_in(self) -> bool:
        return True
    
    def zoom_out(self) -> bool:
        return True
    
    def set_zoom(self, level: int):
        pass
    
    def reset_zoom(self):
        pass
        
MAIN = Camera()

