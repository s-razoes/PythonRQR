import os
#project libraries
import config

files_path = os.path.join(os.getcwd(), config.FILES_PATH)

def id_created(idi):
    path = os.path.join(files_path, idi + config.LOG_PREFIX)
    return os.path.exists(path)

def id_type(idi):
    path = path_link(idi)
    if os.path.exists(path) is True:
        return config.CONTENT_TYPE.LINK
    path = path_value(idi)
    if os.path.exists(path) is True:
        return config.CONTENT_TYPE.VALUE
    path = path_file(idi)
    if os.path.exists(path) is True:
        return config.CONTENT_TYPE.FILE

    return config.CONTENT_TYPE.NONE

def setup_id(idi, data):
    file_path = os.path.join(files_path, idi + config.SET_PREFIX)
    f = open(file_path, "a", encoding='utf8')
    f.write(data)
    f.close()

def is_id_setup(idi):
    path = os.path.join(files_path, idi + config.SET_PREFIX)
    return os.path.exists(path)

def path_link(idi):
    return os.path.join(files_path, idi + config.LINK_PREFIX)

def path_value(idi):
    return os.path.join(files_path, idi + config.VAL_PREFIX)

def path_file(idi):
    return os.path.join(files_path, idi + config.FILE_PREFIX)

def write_data(idi, data, type, filename=None):
    if type is config.CONTENT_TYPE.FILE:
        file_path = path_file(idi)
        data.save(file_path)
        data = filename
        type = config.CONTENT_TYPE.VALUE
    f = None
    if type is config.CONTENT_TYPE.VALUE:
        file_path = path_value(idi)
    if type is config.CONTENT_TYPE.LINK:
        file_path = path_link(idi)
    f = open(file_path, "a", encoding='utf8')
    f.write(data)
    f.close()


def load_data(idi, type):
    fileData = None
    if type is config.CONTENT_TYPE.FILE:
        f = open(file_path, "rb")
        fileData = f.read()
    if type is config.CONTENT_TYPE.LINK:
        file_path = path_link(idi)
    else:
        file_path = path_value(idi)
    f = open(file_path, "r")
    valData = f.read()
    return fileData, valData
    
#log to file
def log_data(request, idi, data):
    log_path = os.path.join(files_path, idi + config.LOG_PREFIX)
    f = open(log_path, "a", encoding='utf8')
    f.write(data)
    f.close()