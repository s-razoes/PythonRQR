import redis

# connect to redis
client = redis.Redis(host='localhost', port=6379)

def set_idi_value(idi, value, type):
    client.set(idi, value)
    set_idi_type(idi, type)

def set_idi_type(idi, type):
    client.set(idi + '_t', type)

def get_idi_value(idi):
    val = client.get(idi)
    if val is not None:
        val = val.decode("UTF8")
    return val

def get_idi_type(idi):
    val = client.get(idi + '_t')
    if val is not None:
        val = val.decode("UTF8")
    return val