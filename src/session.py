import pygame

class GameSession():
    
    def __init__(self):
        self.__is_quitting = False
        
    @property
    def is_quitting(self) -> bool:
        if self.__is_quitting:
            return True
        return False
    
    def quit_game(self) -> bool:
        if self.is_quitting:
            return False
        self.__is_quitting = True
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        return True