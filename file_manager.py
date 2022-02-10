import os
#project libraries
import config

files_path = os.path.join(os.getcwd(), config.FILES_PATH)

def id_created(idi):
    path = os.path.join(files_path, idi + config.LOG_PREFIX)
    return os.path.exists(path)

def id_type(idi):
    path = path_file(idi)
    if os.path.exists(path) is True:
        return config.CONTENT_TYPE.FILE
    file_path = path_type(idi)
    if os.path.exists(file_path) is True:
        f = open(file_path, "r", encoding='utf8')
        ch = f.read()[0]
        type = config.CONTENT_TYPE(int(ch))
        return type

    return config.CONTENT_TYPE.NONE

def id_expired(idi):
    file_path = path_type(idi)
    if os.path.exists(file_path) is True:
        f = open(file_path, "r", encoding='utf8')
        ch = f.read()[1:]
        #TODO
        '''
        created_time = os.path.getctime(file_path)
        if ch == "1h":
            os.path.getctime
        if ch == "10min":

        if ch == '1hit':
        if ch == '10hits':
        '''
    return None

def setup_id(idi, data):
    file_path = os.path.join(files_path, idi + config.SET_PREFIX)
    f = open(file_path, "a", encoding='utf8')
    f.write(data)
    f.close()

def is_id_setup(idi):
    path = os.path.join(files_path, idi + config.SET_PREFIX)
    return os.path.exists(path)

def path_value(idi):
    return os.path.join(files_path, idi + config.VAL_PREFIX)

def path_type(idi):
    return os.path.join(files_path, idi + config.TYPE_PREFIX)

def path_file(idi):
    return os.path.join(files_path, idi + config.FILE_PREFIX)

def write_data(idi, data, type):
    file_path = path_value(idi)
    f = open(file_path, "a", encoding='utf8')
    f.write(data)
    f.close()
    if type is not config.CONTENT_TYPE.FILE:
        file_path = path_type(idi)
        f = open(file_path, "w", encoding='utf8')
        f.write(type)
        f.close()

def write_file_data(idi, file):
    file_path = path_file(idi)
    file.save(file_path)
    file.close()

def load_file_data(idi):
    file_path = path_file(idi)
    f = open(file_path, "rb")
    return f.read()

def load_data(idi):
    file_path = path_value(idi)
    f = open(file_path, "r")
    return f.read()

#log to file
def log_data(request, idi, data):
    log_path = os.path.join(files_path, idi + config.LOG_PREFIX)
    f = open(log_path, "a", encoding='utf8')
    f.write(data)
    f.close()