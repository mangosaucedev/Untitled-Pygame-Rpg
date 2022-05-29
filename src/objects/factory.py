from objects import GameObject

from typing import Tuple

def base_object(position: Tuple[int, int] = (0, 0)) -> GameObject:
    return GameObject(position)

def base_rendered_object(position: Tuple[int, int] = (0, 0)) -> GameObject:
    import rendering.textures
    
    from objects.parts_rendering import Renderer
    
    game_object: GameObject = base_object(position)
    
    game_object.parts.add(Renderer(game_object, image=rendering.textures.get("tile_test.png")))
    
    return game_object