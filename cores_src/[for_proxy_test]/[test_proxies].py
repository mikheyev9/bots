import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
s_path = path.split('\\')
s_path.pop()
sys.path.insert(0, '\\'.join(s_path) + '\\cores_src')
from cores import *
from vis import *

class ChromeTab(BotCore):
    def __init__(self, ChrTab):
        super().__init__(ChrTab)
        self.check_proxies()
        
BotCore.proxy_centralized = False
        
Tab = ChromeTab(0)

a = input()