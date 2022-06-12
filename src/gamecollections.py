from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class Grid(Generic[T]):
  
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.content = []
        for _ in range(0, int(self.width)):
            content = []
            for _ in range(0, int(self.height)):
                content.append(None)
            self.content.append(content)
        
    def is_within_bounds(self, x: int, y: int):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def get(self, x: int, y: int) -> Optional[T]:
        if not self.exists(x, y):
            return None
        return self.content[int(x)][int(y)]

    def set(self, x: int, y: int, value: T):
        if self.is_within_bounds(x, y):
            self.content[int(x)][int(y)] = value

    def exists(self, x: int, y: int) -> bool:
        if not self.is_within_bounds(x, y):
            return False
        if self.content[int(x)][int(y)]:
            return True
        return False
    
    def __getitem__(self, x: int) -> list[T]:
        return self.content[x]