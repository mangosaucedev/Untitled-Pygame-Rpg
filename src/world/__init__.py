import debug

from abc import ABC, abstractmethod
from game_collections import Grid
from typing import List, Tuple

TILE_WIDTH = 64
TILE_HEIGHT = 64
WORLD_SIZE = 24
ZONE_SIZE = 64

class World():
    
    def __init__(self, size: Tuple[int, int] = (WORLD_SIZE, WORLD_SIZE)):
        self.size: Tuple[int, int] = size
        
        width, height = size
        self.zones: Grid[Zone] = Grid[Zone](width, height)
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.zones.set(x, y, Zone((x, y)))
        
        self.builders: List[WorldBuilder] = list()
        self.is_built: bool = False
        self.current_zone: Zone = None
        
    def build(self):
        if self.is_built:
            return
        debug.log("[WORLD] - Building world...")
        
        while self.builders.__len__() > 0:
            builder = self.builders.pop(0)
            builder.build()
            
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                zone = self.zones.get(x, y)
                zone.build()
            
        debug.log("[WORLD] - World built!")   
            
        self.go_to_zone((0, 0))  
                
    def go_to_zone(self, position: Tuple[int, int]) -> bool:
        x, y = position
        if self.zones.is_within_bounds(x, y):
            debug.log(f"[WORLD] - Going to zone @ {x}, {y}")
            zone = self.zones.get(x, y)
            self.current_zone = zone
            return True
        return False
        
class WorldBuilder(ABC):
    
    def __init__(self, world: World):
        self.world: World = world
        
    @abstractmethod
    def build(self):
        pass
        
class Zone():
    
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int] = (ZONE_SIZE, ZONE_SIZE)):
        from objects import Cell 
        self.position = position
        self.size = size
        
        width, height = size
        self.cells: Grid[Cell] = Grid[Cell](width, height)
        
        self.builders: List[ZoneBuilder] = list()
        self.is_built: bool = False
        
    def build(self):
        if self.is_built:
            return
    
class ZoneBuilder(ABC):
    
    def __init__(self, zone: Zone):
        self.zone: Zone = zone
        
    @abstractmethod
    def build(self):
        pass
    
current_world: World = None
    
def go_to_world(world: World):    
    global current_world
    
    current_world = world
    current_world.build()