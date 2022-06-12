import debug
import json
import os

from enum import Enum
from typing import Dict, List

TEXTURES_PATH = os.path.abspath(os.path.join("assets", "__core", "textures"))
DATA_PARENT_PATH = os.path.abspath("data")

class Category(Enum):
    OBJECTS = "objects"

__DATA_CATEGORIES = [
        Category.OBJECTS.value
    ]

class DataEntry():
    
    def __init__(self, category: str, full_path: str, name: str, data):
        self.category: str = category
        self.full_path: str = full_path
        self.name: str = name
        self.data = data

__DATA_ENTRIES_BY_CATEGORY: Dict[str, Dict[str, DataEntry]] = dict()

def get_data_entry(category: Category, name: str) -> DataEntry:
    return __DATA_ENTRIES_BY_CATEGORY[category.value][name]

def __load_all():
    for category in __DATA_CATEGORIES:
        category_data =  __load_all_in_category(category)
        __DATA_ENTRIES_BY_CATEGORY[category] = category_data
        debug.log(f"[DATA] - {category_data.__len__()} data entries loaded from category \"{category}\"")
        
def __load_all_in_category(category: str) -> Dict[str, DataEntry]:
    category_data: Dict[str, DataEntry] = dict()
    directories: List[str] = list()
    __get_all_directories_with_name(DATA_PARENT_PATH, category, directories)
    
    paths: List[str] = list()
    for directory in directories:
        __get_all_data_paths_within_directory(directory, paths)
        
    for path in paths:
        with open(path, "r") as file:
            data = json.load(file)
            name = data["name"]
            data_entry: DataEntry = DataEntry(category, path, name, data)
            category_data[name] = data_entry
    
    return category_data
    
def __get_all_directories_with_name(rootdir:str, target: str, directories: List[str]):
    
    for entry in os.scandir(rootdir):
        if entry.is_dir():
            if entry.name == target:
                directories.append(entry.path)
            __get_all_directories_with_name(entry.path, target, directories)
            
def __get_all_data_paths_within_directory(rootdir:str, paths: List[str]):
    for entry in os.scandir(rootdir):
        if entry.is_dir():
            __get_all_data_paths_within_directory(entry.path, paths)
        elif entry.name.endswith(".json"):
            paths.append(entry.path)
            
__load_all()
            