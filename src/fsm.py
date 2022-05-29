from abc import ABC
from typing import List, Optional

class StateMachine(ABC):
    
    def __init__(self):
        self.state = None
        self.transitions: List[Transition] = list()
        self.transitionsfromany: List[TransitionFromAny] = list()
    
    def update(self):
        if self.__update_transitions_from_any() or self.__update_transitions():
            return
        if self.state:
            self.state.update()
    
    def go_to_state(self, state):
        if self.state:
            self.state.end()
        
        self.state = state
        
        if self.state:
            self.state.start()
            
        self.update()

    def __update_transitions_from_any(self) -> bool:
        for trans in self.transitionsfromany:
            if trans and trans.can_transition():
                self.go_to_state(trans.end)
                return True 
        return False

    def __update_transitions(self):
        for trans in self.transitions:
            if trans and self.state == trans.start and trans.can_transition():
                self.go_to_state(trans.end)
                return True
        return False

class State(StateMachine, ABC): 
    
    def start(self):
        pass
    
    def end(self):
        pass
  
class TransitionFromAny():
    
    def __init__(self, func, end = None):
        self.end: Optional[State] = end
        self.func = func
        
    def can_transition(self) -> bool:
        can_transition: bool = self.func()
        return can_transition
    
class Transition(TransitionFromAny):
    
    def __init__(self, func, start = None, end = None):
        super().__init__(end, func)
        
        self.start: Optional[State] = start