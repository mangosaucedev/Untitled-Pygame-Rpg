import debug
import fsm
import inputs.evaluators
import main
import pygame

from abc import ABC
from autoupdate import auto_updater, Order
from fsm import Transition, TransitionFromAny
from typing import Optional

def poll_events() -> bool:
    import inputs.keys as keys
    
    events = pygame.event.get()
    
    for event in events:
            
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            keys.update_pressed(event)
        if event.type == pygame.KEYUP:
            keys.update_released(event)
            
    INPUT_STATE_MACHINE.update()
    return True
   
class InputState(fsm.State, ABC):
    
    def __init__(self):
        super().__init__()
        self.evaluators = []
    
    def start(self):
        super().start()
        debug.log(str.format('[INPUT STATE] - Input state enabled: {0}', type(self).__name__))

    def update(self):
        super().update()
        for evaluator in self.evaluators:
            if not evaluator.evaluate():
                return
    
class GameplayState(InputState):
        
    def __init__(self):
        super().__init__()
        self.evaluators.append(inputs.evaluators.QuitEvaluator( ))
        self.evaluators.append(inputs.evaluators.MovementEvaluator())
        
class InputStateMachine(fsm.StateMachine):
    
    def __init__(self):
        super().__init__()
        self.gameplay_state: InputState = GameplayState()
        
    @property
    def input_state(self) -> Optional[InputState]:
        return self.state

    @auto_updater(order=Order.UPDATE)
    def update(self):
        super().update()
            
INPUT_STATE_MACHINE: InputStateMachine = InputStateMachine()
