import objects.factory

from objects import GameObject

__instance: GameObject = None

def get_instance(blueprint: str = "player") -> GameObject:
    global __instance 
    
    if not __instance:
        __instance = objects.factory.build(blueprint)
    return __instance