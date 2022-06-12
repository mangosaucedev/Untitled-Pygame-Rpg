from dataclasses import dataclass
from objects import Cell, GameObject

@dataclass 
class BeforeLeaveCellMessage:
    object: GameObject
    cell: Cell

@dataclass 
class LeaveCellMessage:
    object: GameObject
    cell: Cell

@dataclass 
class AfterLeaveCellMessage:
    object: GameObject
    cell: Cell

@dataclass 
class BeforeEnterCellMessage:
    object: GameObject
    cell: Cell

@dataclass 
class EnterCellMessage:
    object: GameObject
    cell: Cell

@dataclass 
class AfterEnterCellMessage:
    object: GameObject
    cell: Cell

@dataclass
class BeforeMoveMessage:
    object: GameObject

@dataclass
class MoveMessage:
    object: GameObject

@dataclass 
class AfterMoveMessage:
    object: GameObject