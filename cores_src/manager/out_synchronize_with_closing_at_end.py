import os
import sys
import json

import BotManager
from vis import *

os.system('color 70')

def grab_enter():
    while True:
        _ = input()
        synchronizer_thread.locker = False

if __name__ == '__main__':
    synchronizer_thread = BotManager.BotSynchronizer(delay=60, del_priority='out', close_at_end=True)
    synchronizer_thread.start()
    Threadize(grab_enter)