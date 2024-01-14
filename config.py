import os
from enum import Enum

crtFile = "fullchain.pem" #if not found or these files don't exist then it will only use http:
keyFile = "privkey.pem"
defaultPort = 80 #if none is selected, then use the automatic ports
localIp = '0.0.0.0' #local ip to listen to, this also means it will only work for IPv4
REDIS = False #True #if redis is true, then files will be ignored and there will be no persistence

#not necessary but possible to change by the user
FILES_PATH = "DATA"
ID_SIZE = 30
KEY_SIZE = 60
KEY_PREFIX =  ".key"
VAL_PREFIX =  "_val.txt"
LINK_PREFIX =  "_lnk.txt"
LOG_PREFIX = "_log.txt"
SET_PREFIX = "_set.txt"
TYPE_PREFIX = "_typ.txt"
FILE_PREFIX = "_file.bin"

LOG_TO_FILE = True
MAX_FILE_SIZE = 20

secure = False
if crtFile != None and keyFile != None and os.path.isfile(crtFile) and os.path.isfile(keyFile):
    secure = True

class CONTENT_TYPE(Enum):
    NONE = 0
    VALUE = 1
    LINK = 2
    FILE = 3
    DELETED = 4
