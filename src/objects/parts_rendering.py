import pygame
import rendering

from objects import GameObject, Part

class Renderer(Part, rendering.RenderObject):
    
    def __init__(self, parent: GameObject, image: pygame.Surface = pygame.Surface([1, 1]), order: int = rendering.RenderOrder.OBJECTS):
        Part.__init__(self, parent)
        rendering.RenderObject.__init__(self, image, order)