import world

from objects import Cell, GameObject, Part, buildable_part
from typing import Tuple

@buildable_part("movement")
class Movement(Part):
    
    def __init__(self, parent: GameObject):
        Part.__init__(self, parent)
        
    def try_move(self, direction: Tuple[int, int]) -> bool:
        ox, oy = self.position
        dx, dy = direction
        new_position = (ox + dx, oy + dy)
        return True