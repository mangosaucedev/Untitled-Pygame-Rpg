import data
import inspect
import objects
import sys

from objects import GameObject

from typing import Tuple

def build(name: str, position: Tuple[int, int] = (0, 0)) -> GameObject:
    
    data_entry: data.DataEntry = data.get_data_entry(data.Category.OBJECTS, name)
    obj_data = data_entry.data
    
    if "inherits" in obj_data:
        game_object: GameObject = build(obj_data["inherits"], position)
    else:
        game_object: GameObject = GameObject(position)
    
    if "parts" in obj_data:
        for part in obj_data["parts"]:
            __add_part_data(game_object, part, obj_data["parts"][part])
    
    if "remove" in obj_data:
        for part in obj_data["remove"]:
            __remove_part(game_object, part)
    
    return game_object
    
def __add_part_data(game_object: GameObject, alias: str, part_data):
    cls = __get_buildable_part_class(alias)
    
    has, part = game_object.parts.try_get(cls)
    
    if not has:
        part = cls(game_object)
        game_object.parts += part
    
    for attribute in part_data:
        value = part_data[attribute]
        part.__setattr__(attribute, value)
        
def __get_buildable_part_class(alias: str):
    return objects.buildable_parts[alias]
    
def __remove_part(game_object: GameObject, part):
    pass

def base_object(position: Tuple[int, int] = (0, 0)) -> GameObject:
    return GameObject(position)

def base_rendered_object(position: Tuple[int, int] = (0, 0)) -> GameObject:
    import rendering.textures
    
    from objects.partsrendering import Renderer
    
    game_object: GameObject = base_object(position)
    
    game_object.parts.add(Renderer(game_object, image=rendering.textures.get("tile_test.png")))
    
    return game_object