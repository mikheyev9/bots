import os
import sys
import time
import socket
import threading
import traceback

path = os.path.dirname(os.path.abspath(__file__))
s_path = path.split('\\')
s_path.pop()
root_path = '\\'.join(s_path)
sys.path.insert(0, root_path + '\\[MySources]')

from vis import *

#from PyQt5 import QtWidgets, QtGui, QtCore, uic
#from qt_forms import Ui_MainWindow

port = 9093

import BotManager
BotManager.start_manager(port)