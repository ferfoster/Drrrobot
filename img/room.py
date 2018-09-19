# -*- coding:utf-8 -*-
import drrrobot
import os
import threading
import time
from urllib.request import URLopener
import os


name = 'pamonha' 
icon = 'zaika' 
file_name = 'niji.cookie'
url_room = 'https://drrr.com/lounge' 
niji = drrrobot.Bot(name=name,icon=icon)

# Night Tips Thread
t_tips = threading.Thread(target=niji.tips)
t_tips.start()

# Main
while 1:
    try:
        if not os.path.isfile(file_name):
            niji.login()
            niji.save_cookie(file_name=file_name)
            if is_leave == True:
                break
        else:
            niji.load_cookie(file_name=file_name)
            if is_leave == True:
                break
        time.sleep(10)
    except BaseException as e:
        print(e)
        print("[--ERR0--]")
