import debug
import fsm
import inputs.evaluators
import main
import pygame

from abc import ABC
from typing import Optional

def poll_events() -> bool:
        
    events = pygame.event.get()
    
    for event in events:
            
        if event.type == pygame.QUIT:
            return False
     
    return handle_keys()

def handle_keys() -> bool:
    
    keys_pressed = pygame.key.get_pressed()
    INPUT_STATE_MACHINE.handle_keys(keys_pressed)
    return True
   
class InputState(fsm.State, ABC):
    
    def __init__(self):
        super().__init__()
        self.evaluators = []
    
    def start(self):
        super().start()
        debug.log(str.format('[INPUT STATE] - Input state enabled: {0}', type(self).__name__))

    def handle_keys(self, keys_pressed):
        if self.state:
            self.state.handle_keys(keys_pressed)
    
class GameplayState(InputState):
        
    def __init__(self):
        super().__init__()
        self.evaluators.append(inputs.evaluators.MovementEvaluator())
        
    def handle_keys(self, keys_pressed):
        if keys_pressed[pygame.K_ESCAPE]:
            main.SESSION.quit_game()
            return
        
        for evaluator in self.evaluators:
            if not evaluator.evaluate(keys_pressed):
                return
        
        super().handle_keys(keys_pressed)
        
class InputStateMachine(fsm.StateMachine):
    
    def __init__(self):
        super().__init__()
        self.gameplay_state: InputState = GameplayState()
        
    @property
    def input_state(self) -> Optional[InputState]:
        return self.state
    
    def handle_keys(self, keys_pressed):
        if self.input_state:
            self.input_state.handle_keys(keys_pressed)
        self.update()
            
INPUT_STATE_MACHINE: InputStateMachine = InputStateMachine()
