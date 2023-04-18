import os
import BotManager

os.system('color 70')
from vis import *

def grab_enter():
    while True:
        _ = input()
        synchronizer_thread.locker = False
            
synchronizer_thread = BotManager.BotSynchronizer(delay=60, del_priority='nodel', close_at_end=True)
synchronizer_thread.start()
Threadize(grab_enter)