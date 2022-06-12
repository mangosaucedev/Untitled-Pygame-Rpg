import debug
import importlib
import json
import os

def __auto_import():
    with open("autoimport.json") as file:
        imports = json.load(file)
        i = 0
        for module in imports:
            importlib.import_module(module)
            i += 1
        debug.log(f"[AUTO IMPORT] - {i} modules imported")
        
__auto_import()