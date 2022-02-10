import config
import file_manager
import redis_manager


def write_data(idi, data, type):
    if config.REDIS:
        return redis_manager.set_idi_value(idi, data, type)

    file_manager.write_data(idi, data, type)

def write_file_data(idi, file, filename, filetype):
    write_data(idi, filename + '|' + filetype, config.CONTENT_TYPE.FILE)
    file_manager.write_file_data(idi,file)

def load_file_data(idi):
    return file_manager.load_file_data(idi)

def load_data(idi, type):
    valData = file_manager.load_data(idi)

    if type is config.CONTENT_TYPE.LINK:
        ltxt = valData.lower()
        if ltxt[:7] != "http://" and ltxt[:8] != "https://":
            valData = "https://" + valData
    return valData

def is_expired(idi):
    file_manager.is_expired(idi)
    return False

def setup_id(idi, data):
    if config.REDIS:
        return redis_manager.set_idi_value(idi + '_setup', data)
    file_manager.setup_id(idi, data)

def is_id_setup(idi):
    if config.REDIS:
        return redis_manager.get_idi_value(idi + '_setup') is not None
    return file_manager.is_id_setup(idi)


def id_type(idi):
    if config.REDIS:
        type = redis_manager.get_idi_type(idi)
        if type is None:
            return 0
        return type
    return file_manager.id_type(idi)

def id_created(idi):
    if config.REDIS:
        return redis_manager.get_idi_type(idi) is not None
    return file_manager.id_created(idi)

def create_id(idi):
    if config.REDIS:
        redis_manager.set_idi_type(idi, '0')
    return file_manager.id_created(idi)