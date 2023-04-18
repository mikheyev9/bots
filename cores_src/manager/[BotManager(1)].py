import os
import sys
import time
import traceback

path = os.path.dirname(os.path.abspath(__file__))
s_path = path.split('\\')
s_path.pop()
root_path = '\\'.join(s_path)
sys.path.insert(0, root_path + '\\[MySources]')

from vis import *

#from PyQt5 import QtWidgets, QtGui, QtCore, uic
#from qt_forms import Ui_MainWindow

port = 9091

import notification_server
threading.Thread(target=notification_server.start_server).start()

import BotManager
BotManager.start_manager(port)