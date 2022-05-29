from abc import ABC, abstractmethod
from typing import List

class Element(ABC):
    
    def __init__(self):
        self.view = None
        
class Selectable(Element):
    
    def __init__(self):
        super().__init__()
    
    def select(self) -> bool:
        if self.is_selected:
            return False
        global selected_element
        
        selected_element = self
        self.__on_select()
        return True
    
    @abstractmethod
    def __on_select(self):
        pass
    
    def deselect(self) -> bool:
        if not self.is_selected:
            return False
        global selected_element
        
        selected_element = None
        self.__on_deselect()
        return True
    
    @abstractmethod
    def __on_deselect(self):
        pass
    
    def is_selectable(self) -> bool:
        return True
    
    @property
    def is_selected(self) -> bool:
        return selected_element == self

class View():

    def __init__(self, layout: List[Element] = list()):
        self.layout: List[Element] = layout
        
        for element in layout:
            element.view = self
            
active_views: List[View] = list()
selected_element: Selectable = None

def select(selectable: Selectable) -> Selectable:
    if not selectable:
        if selected_element:
            selected_element.deselect()
        return None
    if selected_element:
        if not selected_element.deselect():
            return selected_element
    selectable.select()
    return selected_element