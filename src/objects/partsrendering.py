import pygame
import rendering

from objects import GameObject, Part, buildable_part

@buildable_part("renderer")
class Renderer(Part, rendering.RenderObject):
    
    def __init__(self, parent: GameObject, *, image: pygame.Surface = pygame.Surface([1, 1]), order: int = rendering.RenderOrder.OBJECTS):
        self.__texture: str = ""
        
        Part.__init__(self, parent)
        rendering.RenderObject.__init__(self, image, order)
        
    @property 
    def texture_override(self) -> str:
        return self.__texture
    
    @texture_override.setter
    def texture_override(self, texture_name: str):
        import rendering.textures
        
        self.sprite = rendering.textures.get(texture_name)
        self.__texture = texture_name
        
            