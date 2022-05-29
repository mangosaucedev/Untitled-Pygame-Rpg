import pygame

from abc import ABC, abstractmethod

class Evaluator(ABC):
    
    @abstractmethod
    def evaluate(self, keys_pressed) -> bool:
        pass
    
class MovementEvaluator(Evaluator):
    
    def evaluate(self, keys_pressed) -> bool:
        dx, dy = (0, 0)
        
        if keys_pressed[pygame.K_w]:
            dy += -1
        if keys_pressed[pygame.K_s]:    
            dy += 1
        if keys_pressed[pygame.K_a]:
            dx += -1
        if keys_pressed[pygame.K_d]:    
            dx += 1    
            
        direction = (dx, dy)    
        
        if not direction == (0, 0):
            import rendering.camera
            rendering.camera.MAIN.move(direction)
            
        return True