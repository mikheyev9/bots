import os
import sys
import json
import time
import random

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

path = os.path.dirname(os.path.abspath(__file__))
s_path = path.split('\\')
s_path.pop()
sys.path.insert(0, '\\'.join(s_path) + '\\cores_src')

from cores import *
from vis import *

inc = 0

needed_events = [
    ('ЦСКА - СКА. Москва. 08 Апр 19:30', 'andrey;valera', 'https://tickets.cska-hockey.ru/?id_event=912')
]

class ChromeTab(BotCore):
    delay = 10

    def __init__(self, ChrTab, event_name, URL, bot_name, *args):
        super().__init__(ChrTab)
        self.event_name = event_name
        self.URL = URL
        self.bot_name = bot_name
        self.args = args

    def body(self):
        self.first_check(By.ID, 'sub-title')
        has_free = lambda elem: 'free="' in str(elem)
        g_elems = [elem for elem in self.driver.find_elements_by_tag_name('g') if has_free(elem)]
        #if len(g_elems) not in [107, 18, 19]:
        g_count = len(g_elems)
        self.bprint(f'Count of g-elems: {g_count}')
        free = lambda elem: double_split(str(elem), 'free="', '"')
        price = lambda elem: double_split(str(elem), 'price="', '"')
        sectors_dict = { 
            '1': '201', '2': '202', '3': '203', '4': '204',
            '5': '205', '6': '206', '7': '207', '8': '208',
            '9': '209', '10': '210', '11': '211', '12': '212',
            '13': '213', '14': '214',
            '15': '501', '16': '502', '17': '503', '18': '504',
            '19': '505', '20': '506', '21': '507', '22': '508',
            '23': '509', '24': '510', '25': '511', '26': '512',  
            '27': '513', '28': '514'
        }
        sector_nam = lambda elem: double_split(str(elem), 'sector_name="', '"')
        sector_name = lambda elem: sectors_dict[sector_nam(elem)] \
                          if sector_nam(elem) in sectors_dict else sector_nam(elem)
        
        #if '747' not in self.URL:
        #    needed_tickets = ['201', '202', '209', '210', '203', '208']
        #if '696' not in self.URL:
        #    needed_tickets = ['201', '202', '209', '210', '203', '204', '205', '206', '207', '211', '208', '212', '213', '214']
        #else:
        #    needed_tickets = ['202', '209']
        #a_sectors = {sector_name(g): int(free(g)) for g in g_elems if sector_name(g) in needed_tickets}
        a_sectors = {sector_name(g): int(free(g)) for g in g_elems}
        comments = {sector_name(g): '|' + price(g) for g in g_elems if has_free(g)}
        self.change_ticket_state(self.event_name, a_sectors, self.URL, separator='\n', comments=comments)
        return True

TeleCore.tele_centralized = False
BotCore.mode = 'multi'
BotCore.release = True
BotCore.tele_bool = True
BotCore.max_tries = 2
BotCore.proxy_centralized = True
BotCore.driver_source = 'hrenium'

telegram_thread = TeleCore()
telegram_thread.start()

start_bots(needed_events, ChromeTab, False, inc=inc)