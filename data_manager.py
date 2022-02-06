import config
import id_manager
import file_manager
import redis_manager


def write_data(idi, data, type):
    if config.REDIS:
        return redis_manager.set_idi_value(idi, data, type)

    file_manager.write_data(idi, data, type)


def load_data(idi, link=False):
    if config.REDIS:
        txt = redis_manager.get_idi_value(idi)
    else:
        txt = file_manager.load_data(idi, link)

    if link:
        ltxt = txt.lower()
        if ltxt[:7] != "http://" and ltxt[:8] != "https://":
            txt = "https://" + txt
    return txt



def id_link_value(idi):
    if config.REDIS:
        type = redis_manager.get_idi_type(idi)
        if type is None:
            return 0
        return type
    return file_manager.id_link_value(idi)

def id_created(idi):
    if config.REDIS:
        return redis_manager.get_idi_type(idi) is not None
    return file_manager.id_created(idi)

def create_id(idi):
    if config.REDIS:
        redis_manager.set_idi_type(idi, '0')
    return file_manager.id_created(idi)