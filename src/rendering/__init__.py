import pygame
import rendering.camera
import rendering.textures

from abc import ABC, abstractproperty
from enum import IntEnum
from typing import OrderedDict, List, Tuple

WIPE_COLOR = (22, 128, 128)

class RenderOrder(IntEnum):
    TILES = 0
    LIQUID = 1 << 6
    ITEMS = 2 << 6
    OBJECTS = 3 << 6
    CHARACTERS = 4 << 6
    WALLS = 5 << 6
    FOG_OF_WAR = 6 << 6
    GUI = 7 << 6

class RenderGroup(pygame.sprite.Group):
    
    def __init__(self, order: int):
        super().__init__()
        self.order = order
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        self.enabled_sprites: List[pygame.sprite.Sprite] = list()
    
    def draw_group(self):
        draw_sprites = [sprite for sprite in self.sprites() if rendering.camera.MAIN.is_within_frustrum(sprite.rect)]
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            
            if isinstance(sprite, RenderObject):
                sprite.render()
            
            if sprite in draw_sprites:
                self.display_surface.blit(sprite.image, sprite.rect)

class RenderObject(pygame.sprite.Sprite):
    
    def __init__(self, image: pygame.Surface = pygame.Surface([1, 1]), order: int = 0):
        super().__init__()
        
        self.origin: Tuple[int, int] = (0, 0)
        self.sprite = image
        self.order = order
        
    @property
    def order(self) -> int:
        return self.__order
        
    @order.setter
    def order(self, order: int):
        for group in self.groups():
            self.remove(group)
        self.add(rendering.get_render_group(order))
        self.__order = order
        
    @property
    def sprite(self) -> pygame.Surface:
        return self.__sprite
    
    @sprite.setter
    def sprite(self, image: pygame.Surface, origin: Tuple[int, int] = (0, 0)):
        self.origin = origin
        self.image = image
        
        dx, dy = self.get_rendering_position()
        ox, oy = self.origin
        self.rect = self.image.get_rect(center=(dx + ox, dy + oy))
        
        self.__sprite = image
        
    @abstractproperty
    def position(self) -> Tuple[int, int]:
        pass
        
    @position.setter
    def position(self, position: Tuple[int, int]):
        pass
        
    def render(self):
        dx, dy = self.get_rendering_position()
        ox, oy = self.origin
        self.rect.x = dx + ox
        self.rect.y = dy + oy
        super().update(self)
        
    def get_rendering_position(self) -> Tuple[int, int]:
        import world
        
        x, y = self.position
        cx, cy = rendering.camera.MAIN.position
        return ((x - cx) * world.TILE_WIDTH, (y - cy) * world.TILE_HEIGHT)

groups: OrderedDict[int, RenderGroup] = { }

def get_render_group(index: int) -> RenderGroup:
    if not groups.get(index, None):
        groups[index] = RenderGroup(index)
    return groups[index]

def render_window(window):
    window.fill(WIPE_COLOR)
    
    for index in sorted(groups.keys(), key=lambda index: index):
        get_render_group(index).draw_group()

    pygame.display.update()
    
def render_surface(window, texture: pygame.Surface, destination: Tuple[float, float]):
    window.blit(texture, destination)