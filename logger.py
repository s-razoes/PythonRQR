import os
import datetime
#project libraries
import file_manager
import config

def log_call(request, idi, info):
    #log the interaction
    now = datetime.datetime.now()
    current_time = now.strftime("%d/%m/%Y - %H:%M:%S: ")
    txt = info + " - " + current_time + request.remote_addr + "\n" + str(request.headers) + "\n"
    if config.LOG_TO_FILE:
        file_manager.log_data(request, idi, txt)
    else:
        print(str(txt))