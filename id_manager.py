import random
import os
import re
#project libraries
import config
from config import CONTENT_TYPE
import data_manager

ids_index = []

#load ids from files?

def get_rnd_str(length):
    return ''.join(random.choices('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))

def create_id():
    while True:
        idi = get_rnd_str(config.ID_SIZE)
        print(str(idi))
        if id_created(idi) is False:
            data_manager.create_id(idi)
            return idi

def setup_id(idi, data):
    data_manager.setup_id(idi, data)

def is_id_setup(idi):
    return data_manager.is_id_setup(idi)

def is_valid_id(idi):
    if len(idi) != config.ID_SIZE:
        return False
    # check if idi has only numbers and alfa
    if len(re.findall("[0-9|A-z]", idi)) != config.ID_SIZE:
        return False
    return True

def id_created(idi):
    return data_manager.id_created(idi)

def id_has_content(idi, result=None):
    if data_manager.id_type(idi) is config.CONTENT_TYPE.NONE:
        return False
    else:
        return True