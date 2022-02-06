import os
#project libraries
import config

files_path = os.path.join(os.getcwd(), config.FILES_PATH)

def id_created(idi):
    path = os.path.join(files_path, idi + config.LOG_PREFIX)
    return os.path.exists(path)

def id_link_value(idi):
    path = path_link(idi)
    if os.path.exists(path) is True:
        return '1' #link
    path = path_value(idi)
    if os.path.exists(path) is True:
        return '2' #value

    return 0

def path_link(idi):
    return os.path.join(files_path, idi + config.LINK_PREFIX)

def path_value(idi):
    return os.path.join(files_path, idi + config.VAL_PREFIX)

def write_data(idi, data, type):
    f = None
    if type == "2":
        file_path = path_value(idi)
    elif type == "1":
        file_path = path_link(idi)
    f = open(file_path, "a", encoding='utf8')
    f.write(data)
    f.close()


def load_data(idi, link=False):
    if link:
        file_path = path_link(idi)
    else:
        file_path = path_value(idi)

    f = open(file_path, "r")
    return f.read()
    
#log to file
def log_data(request, idi, data):
    log_path = os.path.join(files_path, idi + config.LOG_PREFIX)
    f = open(log_path, "a", encoding='utf8')
    f.write(data)
    f.close()