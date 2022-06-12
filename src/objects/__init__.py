from abc import ABC, abstractmethod, abstractproperty
from typing import List, Protocol, Tuple 

class MessageHandler(Protocol):
    
    def send_message(self, handler, message) -> bool:
        ...

    def handle_message(self, message) -> bool:
        ...

class Cell():
    
    def __init__(self, position: Tuple[int, int]):
        self.position = position
        self.objects: list[GameObject] = list()

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

    def __iadd__(self, game_object):
        if game_object in self.objects:
            return self
        self.objects.append(game_object)
        return self

    def __isub__(self, game_object):
        if not game_object in self.objects:
            return self
        self.objects.remove(game_object)
        return self

    def send_message(self, handler: MessageHandler, message) -> bool:
        return handler.handle_message(message)

    def handle_message(self, message) -> bool:
        successful: bool = True
        for game_object in self.objects:
            if not game_object.handle_message(message):
                successful = False
        return successful

class CellInfo():
    
    def __init__(self, game_object, position: Tuple[int, int] = (0, 0)):       
        self.cell = None
        self.game_object = game_object
        self.position = position

    @property
    def position(self) -> Tuple[int, int]:
        return self.__position
    
    @position.setter
    def position(self, position: Tuple[int, int]):
        import world
        
        from objects.messages import BeforeLeaveCellMessage, LeaveCellMessage, AfterLeaveCellMessage, BeforeEnterCellMessage, EnterCellMessage, AfterEnterCellMessage

        if self.cell:
            if not self.cell.handle_message(BeforeLeaveCellMessage(self.game_object, self.cell)):
                return
            self.cell -= self.game_object
            self.cell.handle_message(LeaveCellMessage(self.game_object, self.cell))
            self.cell.handle_message(AfterLeaveCellMessage(self.game_object, self.cell))

        x, y = position
        if not world.current_world.current_zone.cells.is_within_bounds(x, y):
            return
            
        cell = world.current_world.current_zone.cells[x][y]
        if cell:
            if not cell.handle_message(BeforeEnterCellMessage(self.game_object, self.cell)):
                return
            cell += self.game_object
            cell.handle_message(EnterCellMessage(self.game_object, self.cell))
            cell.handle_message(AfterEnterCellMessage(self.game_object, self.cell))

        self.__position = position
        self.cell = cell
        
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

    @abstractmethod
    def send_message(self, handler: MessageHandler, message) -> bool:
        pass

    @abstractmethod
    def handle_message(self, message) -> bool:
        pass

class GameObject(Object):
    
    def __init__(self, position: Tuple[int, int] = (0, 0)):
        self.parts: PartCollection = PartCollection(self)
        self.cell: CellInfo = CellInfo(self, position)
       
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

    def send_message(self, handler: MessageHandler, message) -> bool:
        return handler.handle_message(message)

    def handle_message(self, message) -> bool:
        successful: bool = True
        for part in self.parts.parts:
            if not part.handle_message(message):
                successful = False
        return successful
        
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

    def send_message(self, handler: MessageHandler, message) -> bool:
        return handler.handle_message(message)

    def handle_message(self, message) -> bool:
        return True

class PartCollection():
    
    def __init__(self, game_object: GameObject):
        self.__game_object = game_object
        self.parts: List[Part] = list()
        
    def __iadd__(self, part: Part):
        if part in self.parts:
            return self
        self.parts.append(part)
        return self

    def has(self, T) -> bool:
        return self.try_get(T)[0]
        
    def try_get(self, T):
        for part in self.parts:
            if isinstance(part, T):
                return True, part
        return False, None
    
    def get(self, T):
        return self.try_get(T)[1]
        
    
all_game_objects: List[GameObject] = []
enabled_game_objects: List[GameObject] = []
buildable_parts = { }

def buildable_part(alias: str):
    def f(cls):
        buildable_parts[alias] = cls
        return cls
    return f