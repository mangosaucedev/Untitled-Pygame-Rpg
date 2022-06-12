import debug
import fsm
import inputs

from abc import ABC, abstractmethod
from autoupdate import auto_updater, Order
from fsm import Transition, TransitionFromAny
from typing import Optional

class GameState(fsm.State, ABC):
    
    def start(self):
        super().start()
        debug.log(str.format('[GAME STATE] - GameState enabled: {0}', type(self).__name__))
    
class InitializeState(GameState):
    
    def __init__(self):
        super().__init__()
    
class LoadingState(GameState):
    
    def __init__(self):
        super().__init__()
    
class GameplayState(GameState):
    
    def __init__(self):
        super().__init__()
        
    def start(self):
        super().start()
        inputs.INPUT_STATE_MACHINE.go_to_state(inputs.INPUT_STATE_MACHINE.gameplay_state)
        
    def end(self):
        super().end()
        inputs.INPUT_STATE_MACHINE.go_to_state(None)

class GameStateMachine(fsm.StateMachine):
    
    def __init__(self):
        super().__init__()
        
        self.initialize_state: GameState = InitializeState()
        self.loading_state: GameState = LoadingState()
        self.gameplay_state: GameState = GameplayState()
        
        self.transitions.append(
            Transition(lambda: True, None, self.gameplay_state))
        
        self.go_to_state(self.initialize_state)

    @property
    def game_state(self) -> Optional[GameState]:
        return self.state

    @auto_updater(order=Order.UPDATE)
    def update(self):
        super().update()

GAME_STATE_MACHINE: GameStateMachine = GameStateMachine()