from typing import Callable, List

class LoadingOperation():
    
    def __init__(self, operation: Callable[[], bool], *, on_completed: Callable = None):
        self.__operation: Callable[[], bool] = operation
        self.__on_completed: Callable = on_completed
        
    def update(self) -> bool:
        if self.__operation():
            if self.__on_completed:
                self.__on_completed()
            return True
        return False
            
current_operation: LoadingOperation = None            

__queue: List[LoadingOperation] = list()

def enqueue(operation: LoadingOperation):
    __queue.append(operation)
    
def update():
    global current_operation
    
    if __queue.__len__() == 0:
        current_operation = None
        return
    current_operation = __queue[0]
    if current_operation.update():
        __queue.pop(0)