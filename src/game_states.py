import debug
import fsm
import inputs

from abc import ABC, abstractmethod
from typing import Optional

class GameState(fsm.State, ABC):
    
    def start(self):
        super().start()
        debug.log(str.format('[GAME STATE] - GameState enabled: {0}', type(self).__name__))
    
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
        self.gameplay_state: GameState = GameplayState()
        self.go_to_state(self.gameplay_state)
        
    @property
    def game_state(self) -> Optional[GameState]:
        return self.state
             
GAME_STATE_MACHINE: GameStateMachine = GameStateMachine()