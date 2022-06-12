import debug
import json
import os

from typing import Dict

def __load_config() -> Dict[str, bool]:
    config_path = os.path.abspath("config.json")
    with open(config_path, "r") as file:
        json_data = file.read()
        debug.log("[CONFIG] - loaded!", debug.DateTimeInfo.FRAME|debug.DateTimeInfo.TIME)
        return json.loads(json_data)
    
settings: Dict[str, bool] = __load_config()

if settings["debugMode"]:
    debug.log("[CONFIG] - Debug mode enabled!", debug.DateTimeInfo.FRAME|debug.DateTimeInfo.TIME)