import debug
import json
import pygame
import os

from autoupdate import auto_updater, Order
from enum import Enum, auto
from events import Event
from typing import Dict

__on_key_pressed: Dict[str, Event] = dict()
__on_key_released: Dict[str, Event] = dict()
__keys_pressed_this_frame: Dict[int, bool] = dict()
__keys_pressed: Dict[int, bool] = dict()
__keys_released_this_frame: Dict[int, bool] = dict()

class KeyCommand(Enum):
    #
    SUBMIT = auto(),
    CANCEL = auto(),
    #Movement
    MOVE_N = auto()
    MOVE_S = auto()
    MOVE_W = auto()
    MOVE_E = auto()
    MOVE_NW = auto()
    MOVE_NE = auto()
    MOVE_SW = auto()
    MOVE_SE = auto()
    MOVE_N_ALT = auto()
    MOVE_S_ALT = auto()
    MOVE_W_ALT = auto()
    MOVE_E_ALT = auto()
    MOVE_PASS = auto()
    
class KeyBinding():
    
    def __init__(self):
        self.keys = [None] * 3
        self.primary_mods = [None] * 3
        self.secondary_mods = [None] * 3

__KEYBINDINGS: Dict[KeyCommand, KeyBinding] = dict()

__DEFAULT_KEYBINDINGS: Dict[str, str] = {
    #
        "SUBMIT": "K_SPACE, , ,K_RETURN",
        "CANCEL": "K_ESCAPE",
    #Movement
        "MOVE_N": "K_KP8",
        "MOVE_S": "K_KP2",
        "MOVE_W": "K_KP4",
        "MOVE_E": "K_KP6",
        "MOVE_NW": "K_KP7",
        "MOVE_NE": "K_KP9",
        "MOVE_SW": "K_KP1",
        "MOVE_SE": "K_KP3",
        "MOVE_N_ALT": "K_UP",
        "MOVE_S_ALT": "K_DOWN",
        "MOVE_W_ALT": "K_LEFT",
        "MOVE_E_ALT": "K_RIGHT",
        "MOVE_PASS": "K_KP5"
    }

__LOADED_KEYBINDINGS = dict()

def __write_default_keybindings():
    path = os.path.join(os.pardir, "keybinds.json")
    with open(path, "w") as file:
        file.write(json.dumps(__DEFAULT_KEYBINDINGS, indent=4))
    debug.log("[KEYS] - Default keybindings written.")

def __load_keybindings() -> bool:
    global __LOADED_KEYBINDINGS
    
    path = os.path.join(os.pardir, "keybinds.json")
    if not os.path.exists(path):
        __write_default_keybindings()
        
    with open(path, "r") as file:
        keybindings = json.load(file)
        if keybindings.__len__() != __DEFAULT_KEYBINDINGS.__len__():
            __LOADED_KEYBINDINGS = __DEFAULT_KEYBINDINGS
            debug.warning("[KEYS] - Keybindings from file out of date; loading defaults.")
            return False
        __LOADED_KEYBINDINGS = keybindings
        debug.log(f"[KEYS] - {__LOADED_KEYBINDINGS.__len__()} keybindings loaded successfully: {__LOADED_KEYBINDINGS}")
    
    __parse_keybindings()
    return True
        
def __parse_keybindings():
    
    for key in __LOADED_KEYBINDINGS:
        entry: str = __LOADED_KEYBINDINGS[key]
        split = entry.split(",")
        _len = split.__len__()
        
        keybinding: KeyBinding = KeyBinding()
        
        if _len > 0:
            keybinding.keys[0] = pygame.__dict__[split[0]]
        if _len > 1 and not split[1].endswith(" "):
            keybinding.primary_mods[0] = pygame.__dict__[split[1]]
        if _len > 2 and not split[2].endswith(" "):
            keybinding.secondary_mods[0] = pygame.__dict__[split[2]]
        if _len > 3:
            keybinding.keys[1] = pygame.__dict__[split[3]]
        if _len > 4 and not split[4].endswith(" "):
            keybinding.primary_mods[1] = pygame.__dict__[split[4]]
        if _len > 5 and not split[5].endswith(" "):
            keybinding.secondary_mods[1] = pygame.__dict__[split[5]]
        if _len > 6:
            keybinding.keys[2] = pygame.__dict__[split[6]]
        if _len > 7 and not split[7].endswith(" "):
            keybinding.primary_mods[2] = pygame.__dict__[split[7]]
        if _len > 8 and not split[8].endswith(" "):
            keybinding.secondary_mods[2] = pygame.__dict__[split[8]]

        __KEYBINDINGS[key] = keybinding
    
    debug.log(f"[KEYS] - {__KEYBINDINGS.__len__()} keybindings parsed successfully: {__KEYBINDINGS.keys()}")  
 
if not __load_keybindings():
    __write_default_keybindings()
    __parse_keybindings()

@auto_updater(order=Order.PRE_UPDATE)
def update():
    __keys_pressed_this_frame.clear()
    __keys_released_this_frame.clear()
    
update()
    
def update_pressed(event):
    key = event.key
    __keys_pressed_this_frame[key] = True
    __keys_pressed[key] = True
    character = event.unicode
    event: Event = get_pressed_event(character)
    if event:
        event()
    
def get_pressed_event(character: str) -> Event:
    if not character:
        return None
    if len(character) > 1:
        character = character[0]
    if not character in __on_key_pressed:
        __on_key_pressed[character] = Event()
    return __on_key_pressed[character]
    
def update_released(event):
    key = event.key
    __keys_pressed[key] = False
    __keys_released_this_frame[key] = True
    character = event.unicode
    event: Event = get_released_event(character)
    if event:
        event()
    
def get_released_event(character: str) -> Event:
    if not character:
        return None
    if len(character) > 1:
        character = character[0]
    if not character in __on_key_released:
        __on_key_released[character] = Event()
    return __on_key_released[character]
                
def pressed(command: KeyCommand) -> bool:
    keybinding: KeyBinding = __KEYBINDINGS[command.name]
    
    for i in range(2):
        key_pressed = __key_pressed(keybinding.keys[i])
        primary_mod_pressed = __key_pressed(keybinding.primary_mods[i], not keybinding.primary_mods[i])
        secondary_mod_pressed = __key_pressed(keybinding.secondary_mods[i], not keybinding.secondary_mods[i])
        if key_pressed and primary_mod_pressed and secondary_mod_pressed:
            return True
    
    return False

def __key_pressed(key: int, not_key: bool = False) -> bool:
    return not_key or __keys_pressed.get(key, False)

def pressed_this_frame(command: KeyCommand) -> bool:
    keybinding: KeyBinding = __KEYBINDINGS[command.name]
    
    for i in range(2):
        key_pressed = __key_pressed_this_frame(keybinding.keys[i])
        primary_mod_pressed = __key_pressed(keybinding.primary_mods[i], not keybinding.primary_mods[i])
        secondary_mod_pressed = __key_pressed(keybinding.secondary_mods[i], not keybinding.secondary_mods[i])
        if key_pressed and primary_mod_pressed and secondary_mod_pressed:
            return True
    
    return False

def __key_pressed_this_frame(key: int, not_key: bool = False) -> bool:
    return not_key or __keys_pressed_this_frame.get(key, False)

def released(command: KeyCommand) -> bool:
    return not pressed(command)

def released_this_frame(command: KeyCommand):
    keybinding: KeyBinding = __KEYBINDINGS[command.name]
    
    for i in range(2):
        if __key_pressed(keybinding.keys[i]):
            return False
    for i in range(2):
        if __keys_released_this_frame.get(keybinding.keys[i], False):
            return True
    return False

