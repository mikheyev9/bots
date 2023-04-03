import os
import sys

s_path = os.path.dirname(os.path.abspath(__file__)).split('\\')[:-1]
sys.path.insert(0, '\\'.join(s_path) + '\\cores_src')
from cores import *
from vis import *
class ChromeTab(BotCore):
    def __init__(self, ChrTab):
        super().__init__(ChrTab)
        self.check_proxies('https://tickets.cska-hockey.ru/', personal=True, verify=False)
        
Tab = ChromeTab(0)