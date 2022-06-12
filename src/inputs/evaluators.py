import inputs.keys as keys
import pygame

from abc import ABC, abstractmethod
from inputs.keys import KeyCommand

class Evaluator(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def evaluate(self) -> bool:
        pass

class QuitEvaluator(Evaluator):

    def evaluate(self) -> bool:
        if keys.pressed_this_frame(KeyCommand.CANCEL):
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return False
        return True

class MovementEvaluator(Evaluator):

    __MOVEMENT_DELAY: float = 0.05
    
    def __init__(self):
        super().__init__()
        self.move_delay: float = 0 
    
    def evaluate(self) -> bool:
        self.__update()

        dx, dy = (0, 0)
        
        if keys.pressed(KeyCommand.MOVE_N) or keys.pressed(KeyCommand.MOVE_N_ALT):
            dy += -1
        if keys.pressed(KeyCommand.MOVE_S) or keys.pressed(KeyCommand.MOVE_S_ALT):
            dy += 1
        if keys.pressed(KeyCommand.MOVE_W) or keys.pressed(KeyCommand.MOVE_W_ALT):
            dx += -1
        if keys.pressed(KeyCommand.MOVE_E) or keys.pressed(KeyCommand.MOVE_E_ALT):
            dx += 1    
            
        if keys.pressed(KeyCommand.MOVE_NW):
            dx, dy = (-1, -1)
        elif keys.pressed(KeyCommand.MOVE_NE):
            dx, dy = (1, -1)
        elif keys.pressed(KeyCommand.MOVE_SW):
            dx, dy = (-1, 1)
        elif keys.pressed(KeyCommand.MOVE_SE):
            dx, dy = (1, 1)
            
        direction = (dx, dy)    
        
        if not direction == (0, 0) and self.move_delay <= 0:
            import objects.player
            
            from objects.partsmovement import Movement
            
            self.move_delay = self.__MOVEMENT_DELAY
            
            player = objects.player.get_instance()
            movement: Movement = player.parts.get(Movement)
            movement.try_move(direction)
            
        return True
    
    def __update(self):
        import clock
        
        if self.move_delay > 0:
            self.move_delay -= clock.delta_time
        