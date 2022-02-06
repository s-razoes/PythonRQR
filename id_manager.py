import random
import os
import re
#project libraries
import config
import data_manager

ids_index = []

#load ids from files?

def get_rnd_str(length):
    return ''.join(random.choices('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))

def create_idi():
    while True:
        idi = get_rnd_str(config.ID_SIZE)
        print(str(idi))
        if id_created(idi) is False:
            data_manager.create_id(idi)
            return idi

def is_valid_idi(idi):
    if len(idi) != config.ID_SIZE:
        return False
    # check if idi has only numbers and alfa
    if len(re.findall("[0-9|A-z]", idi)) != config.ID_SIZE:
        return False
    return True

def id_created(idi):
    return data_manager.id_created(idi)
    #return idi in ids_index

def id_link_value(idi):
    return data_manager.id_link_value(idi)

def id_has_lnk_val(idi, result=None):
    if result is None:
        result = id_link_value(idi)
    if result in ('1','2'):
        return True
    return False