import world

from objects import Cell, GameObject, Part, buildable_part
from typing import Tuple

@buildable_part("movement")
class Movement(Part):
    
    def __init__(self, parent: GameObject):
        super().__init__(parent)
        
    def try_move(self, direction: Tuple[int, int]) -> bool:
        from objects.messages import BeforeMoveMessage, MoveMessage, AfterMoveMessage 

        if not self.send_message(self.parent, BeforeMoveMessage(self.parent)):
            return False

        ox, oy = self.position
        dx, dy = direction
        new_position = (ox + dx, oy + dy)
        self.position = new_position

        self.send_message(self.parent, MoveMessage(self.parent))
        self.send_message(self.parent, AfterMoveMessage(self.parent))
        
        return True
    
    def move(self):
        pass
    
@buildable_part("obstacle")
class Obstacle(Part):
    
    def __init__(self, parent:GameObject):
        super().__init__(parent)
        self.is_passable: bool = False

    def handle_message(self, message) -> bool:
        from objects.messages import BeforeEnterCellMessage

        if isinstance(message, BeforeEnterCellMessage):
            return self.__on_before_enter_cell(message)    

        return super().handle_message(message)

    def __on_before_enter_cell(self, message) -> bool:
        if message.object == self.parent:
            return True
        return self.is_passable