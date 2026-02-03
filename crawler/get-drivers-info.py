from typing import Dict, List, TypedDict, Optional, Any
import time
from pprint import pprint
import os
import json

import requests as r

BASE_URL="https://gfwsl.geforce.com/nvidia_web_services/controller.php?com.nvidia.services.Drivers.getMenuArrays/"
BOARD_TYPES_FILE=os.path.join(".", "board_types.json")
OUTPUT_DATA=os.path.join(".", "drivers_boards_data.json")

class Colors:
    GREEN="\033[42m"
    CYAN="\033[46m"
    RED="\033[41m"
    RESET="\033[0m"

type BoardTypes = Dict[str,int]
class MenuItems(TypedDict):
    _explicitType:str
    id:int|str
    menutext:str

type Items = Optional[List[BoardTypes]]
type CachedData = Dict[str,int]
class ResponseDict(TypedDict):
    board_types:CachedData
    series:CachedData
    boards:CachedData
    _something:CachedData
    systems:CachedData
    langauges:CachedData

def load_board_types() -> BoardTypes:
    with open(BOARD_TYPES_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def save_board_types(board_types:CachedData):
    with open(BOARD_TYPES_FILE, "w", encoding="utf-8") as file:
        json.dump(board_types, file)

def save_data(data:Dict[Any,Any]):
    with open(OUTPUT_DATA, "w", encoding="utf-8") as file:
        json.dump(data, file)

def generate_params(board_type:int, series_id:Optional[int]=None) -> str: 
    if(series_id is None):
        series_id = 'null'
    return ('{'+ f'"pt":"{board_type}","sa":"1","pst":{series_id},"d2":null,"d4":null,"cookieEmpty":false,"driverType":"all"' +'}').replace('"',"%22")

def get_menu_items_from_array(items:Items) -> CachedData:
    if(items is None):
        return {}

    data = {}
    for item in items:
        data[item["menutext"]] = int(item["id"])
    return data

def do_request(board_type:int, series_id:Optional[int]=None) -> ResponseDict:
    params = generate_params(board_type_id,series_id)
    complete_url = f"{BASE_URL}{params}"
    response = r.get(complete_url).json()

    if(len(response) != 6):
        raise ValueError("Invalid Response")

    return {
            "board_types":get_menu_items_from_array(response[0]),
            "series":get_menu_items_from_array(response[1]),
            "boards":get_menu_items_from_array(response[2]),
            "_something":get_menu_items_from_array(response[3]),
            "systems":get_menu_items_from_array(response[4]),
            "languages":get_menu_items_from_array(response[5])
        }

if __name__ == "__main__":
    board_types = load_board_types()
    new_board_types = {}
    data = {}
    
    for name,board_type_id in board_types.items():
        print(Colors.GREEN + "-"*20 + Colors.RESET)
        print(f"{Colors.GREEN}searching for {name}{Colors.RESET}")

        try:
            response = do_request(board_type_id)
        except ValueError:
            print(f"{Colors.RED}--Invalid data from API--{Colors.RESET}")
            continue

        new_board_types = response["board_types"]

        series = response["series"]
        print("Series: ", end="")
        pprint(series)
        print(Colors.CYAN + '#'*20 + Colors.RESET)

        data[name] = {}

        for series_name, series_id in series.items():
            print(f"{Colors.CYAN}\n\nGetting for {series_name}:{series_id} ...\n\n{Colors.RESET}")
        
            try:
                response = do_request(board_type_id,series_id)
            except ValueError:
                print(f"{Colors.RED}--Invalid data from API--{Colors.RESET}")
                continue
            
            print("Boards: ", end="")
            pprint(response["boards"])

            print("Systems: ", end="")
            pprint(response["systems"])

            print("Languages: ", end="")
            pprint(response["languages"])

            data[name][series_name] = {
                    "id": series_id,
                    "boards": response["boards"],
                    "systems": response["systems"],
                    "languages":response["languages"]
            }
        
            time.sleep(2)
    
    print(f"{Colors.GREEN}Saving data...{Colors.RESET}")
    save_board_types(new_board_types)
    save_data(data)
