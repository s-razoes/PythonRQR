import random
import re
#project libraries
import config
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

def delete_id(idi):
    data_manager.delete_id(idi)

def setup_id(idi, data):
    key = get_rnd_str(config.KEY_SIZE)
    data_manager.setup_id(idi, key, data)
    return key

def check_key(idi, key):
    return data_manager.check_key(idi, key)

def is_id_setup(idi):
    return data_manager.is_id_setup(idi)

def is_expired(idi):
    return data_manager.is_expired(idi)

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