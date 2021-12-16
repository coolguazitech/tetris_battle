import socket
import threading
import time
import pygame as pg
from set import Set
from main_screen import Main_screen
from game_room import Game_room
import db_utils

# VERSION
VERSION = "1.0.0"

def check_up_to_date(version):
    """version check routine, access database"""
    db_utils.create_table()
    old_dict_info = db_utils.fetch(1)
    
    if old_dict_info["VERSION"] != version:
        # TODO: update new_dict_info
        new_dict_info = {
            "BADGE": old_dict_info["BADGE"],
            "SCORE": old_dict_info["SCORE"],
            "VERSION": version,    
            "DATE": time.ctime(),
        }
        db_utils.update(1, new_dict_info)
        


if __name__ == '__main__':
    check_up_to_date(VERSION)
    set = Set(VERSION)
    set.register_scene(Main_screen())
    set.register_scene(Game_room())
    set.run()

