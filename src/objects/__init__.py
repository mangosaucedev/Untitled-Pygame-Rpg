from abc import ABC, abstractproperty
from typing import List, Optional, Tuple 

class Cell():
    
    def __init__(self, position: Tuple[int, int]):
        self.position = position

    @property
    def position(self) -> Tuple[int, int]:
        return self.__position
    
    @position.setter
    def position(self, position: Tuple[int, int]):
        self.__position = position
        
    @property
    def x(self) -> int:
        return self.position[0]
        
    @property
    def y(self) -> int:
        return self.position[0]

class CellInfo():
    
    def __init__(self, position: Tuple[int, int] = (0, 0)):
        self.position = position
    
    @property
    def position(self) -> Tuple[int, int]:
        return self.__position
    
    @position.setter
    def position(self, position: Tuple[int, int]):
        self.__position = position
        
    @property
    def x(self) -> int:
        return self.position[0]
    
    @x.setter
    def x(self, x: int):
        self.position = (x, self.position[1])
        
    @property
    def y(self) -> int:
        return self.position[0]
    
    @y.setter
    def y(self, y: int):
        self.position = (self.position[0], y)      

class Object(ABC):
    
    def __init__(self):
        self.is_enabled: bool = False
        self.enable()
        
        self.is_alive = True
        
        self.is_started: bool = False
        self.__start()
    
    @abstractproperty
    def position(self) -> Tuple[int, int]:
        pass
    
    @position.setter
    def position(self, position: Tuple[int, int]):
        pass
    
    def __start(self) -> bool:
        if self.is_started:
            return False
        self.is_started = True
        
    def enable(self) -> bool:
        if self.is_enabled:
            return False
        self.is_enabled = True
        self.__on_enable()
        return True
    
    def __on_enable(self):
        pass
            
    def disable(self) -> bool:
        if not self.is_enabled:
            return False
        self.is_enabled = False
        self.__on_disable()
        return True
    
    def __on_disable(self):
        pass
    
    def update(self):
        pass
    
    def destroy(self) -> bool:
        if not self.is_alive:
            return False
        self.disable()
        self.is_alive = False
        self.__on_destroy()
    
    def __on_destroy(self):
        pass

class GameObject(Object):
    
    def __init__(self, position: Tuple[int, int] = (0, 0)):
        self.cell = CellInfo(position)
        self.parts = PartCollection(self)
        super().__init__()
        all_game_objects.append(self)
        
    @property
    def position(self) -> Tuple[int, int]:
        return self.cell.position
    
    @position.setter
    def position(self, position: Tuple[int, int]):
        self.cell.position = position        
        
    def update(self):
        for part in self.parts.parts:
            part.update()    
        
    def __on_enable(self):
        super().__on_enable()
        enabled_game_objects.append(self)
        for part in self.parts.parts:
            part.enable()    
            
    def __on_disable(self):
        super().__on_disable()
        enabled_game_objects.remove(self)
        for part in self.parts.parts:
            part.disable()    
    
    def __on_destroy(self):
        super().__on_disable()
        for part in self.parts.parts:
            part.destroy()
        all_game_objects.remove(self)
        
class Part(Object):
        
    def __init__(self, parent: GameObject):
        self.parent = parent
        super().__init__()
        
    @property
    def position(self) -> Tuple[int, int]:
        return self.parent.position
    
    @position.setter
    def position(self, position: Tuple[int, int]):
        self.parent.position = position

class PartCollection():
    
    def __init__(self, game_object: GameObject):
        self.__game_object = game_object
        self.parts: List[Part] = list()
        
    def add(self, part: Part) -> bool:
        if part in self.parts:
            return False
        self.parts.append(part)
        return True
    
    def has(self, T) -> bool:
        return self.try_get(T)[0]
        
    def try_get(self, T):
        for part in self.parts:
            if isinstance(part, T):
                return True, part
        return False, None
    
all_game_objects: List[GameObject] = []
enabled_game_objects: List[GameObject] = []
buildable_parts = { }

def buildable_part(alias: str):
    def f(cls):
        buildable_parts[alias] = cls
        return cls
    return f