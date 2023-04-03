import os
import sys
import json
import time
import socket
import random
import threading

from .vis import *


class ManagerClient(threading.Thread):
    def __init__(self, client_name, tabs, accounts, port, is_buying_bot):
        threading.Thread.__init__(self)
        self.client_name = client_name
        self.port = port
        self.tabs = tabs
        self.accounts = accounts
        self.first_size = 0
        self.first_check = False
        self.thread_timer = 600 if is_buying_bot else 1800
        self.second_thread_timer = 500 if is_buying_bot else 1500
        try:
            self.init_success = True
            from get_ip import get_local_ip
            self.client = socket.socket()
            self.client.connect((get_local_ip(), self.port))
            self.send(self.client_name)
            print('Successfully connected to bot manager')
        except:
            self.init_success = False
            print('Error connecting to the bot manager! Switching to offline mode')
            
    def __str__(self):
        try:
            self.send('alive')
        except:
            return 'Нарушена связь сокета с ботмэнэджером!'
        if not self.accounts:
            return f'Бот работает без использования аккаунтов.\n' \
                   f'Кол-во потоков бота в сокете - {len(self.tabs)}'
        return f'Изначальное кол-во аккаунтов - {self.first_size}\n' \
               f'Текущее кол-во аккаунтов - {self.accounts.ready.qsize()}\n' \
               f'Account first check - {self.first_check}\n' \
               f'Кол-во потоков бота в сокете - {len(self.tabs)}'
            
        
    def read(self):
        data = self.client.recv(1024)
        return data.decode('utf-8')
        
    def send(self, mes):
        self.client.send(mes.encode('utf-8'))
        
    def double_check(self, break_threads, count_errors):
        for bot in self.tabs:
           if (time.time() - bot.last_time_body) >= self.second_thread_timer:
                thread = f'{bot.event_name} - {bot.URL}'
                break_threads.append(thread)
                count_errors += 1
                bot.last_time_body = time.time()
        return count_errors
    
    def run(self):
        if not self.init_success:
            return False
        try:
            while True:
                if self.accounts and self.accounts.accounts_check:
                    self.first_size = self.accounts.ready.qsize()
                    self.accounts.accounts_check = False
                    self.first_check = True
                break_threads = []
                send_mes = 'alive'
                count_errors = 0
                mes = self.read()
                if mes == 'are_you_alive':
                    if self.first_check and (self.accounts.ready.qsize()) < (self.first_size*0.3):
                        account_time_error = time.time()
                        self.first_check = False
                    if self.first_size and not self.first_check:
                        if time.time() - account_time_error > 600:
                            if (self.accounts.ready.qsize()) < (self.first_size*0.3):
                                self.send('accounts')
                                lprint(f'SOCKET INFO:\n'
                                       f'Изначальное кол-во аккаунтов - {self.first_size}\n'
                                       f'Текущее кол-во аккаунтов - {self.accounts.ready.qsize()}')
                            self.first_check = True
                            continue
                    for bot in self.tabs:
                        if (time.time() - bot.last_time_body) >= self.thread_timer:
                            count_errors = self.double_check(break_threads, count_errors)
                            break
                    if (count_errors == len(self.tabs)) and (count_errors!=0):
                        self.send('all')
                    elif break_threads:
                        send_mes = '\n'.join(break_threads)
                        self.send(send_mes)
                    else:
                        self.send(send_mes) 
                if mes == 'shutdown':
                    print('An error occured while reading messages from manager. Killing socket.')
                    raise SystemExit
        except:
            print('An error occured while reading messages from manager. Killing socket.')
            raise SystemExit


def find_port(bot_name):
    root_path = os.path.dirname(os.path.abspath(__file__))
    with open(f'{root_path}\\[config].json', 'r') as f:
        payload = f.read()
    lines = payload.split('\n')
    lines = [line for line in lines if '#' not in line[:4]]
    last_line = lines[-2]
    if last_line[-1] == ',':
        without_comma = last_line[:-1]
        lines[-2] = without_comma
    payload = '\n'.join(lines)
    config = json.loads(payload)
    for time, name, port in config:
        if bot_name == name:
            return port
              
              
def change_dir():
    script_name = sys.argv[0]
    path_bits = script_name.split('\\')[:-1]
    work_dir = '\\'.join(path_bits)
    if work_dir:
        os.chdir(work_dir)


def change_bot_name(bot_name, is_buying_bot):
    if len(sys.argv) != 3:
        port = find_port(bot_name)
        return bot_name, port
    if int(sys.argv[1]) and int(sys.argv[2]):
        bot_name += '_be'
        port = find_port(bot_name)
        if is_buying_bot:
            bot_name += '/buybot'
        else:
            bot_name += '/evbot'
    elif int(sys.argv[1]) and not int(sys.argv[2]):
        bot_name += '_b'
        port = find_port(bot_name)
    else:
        bot_name += '_e'
        port = find_port(bot_name)
    return bot_name, port
    
    
def run_socket(tabs, accounts=None, is_buying_bot=False):
    change_dir()
    script_name = sys.argv[0]
    path_items = script_name.split('.')[:-1]
    bot_name = '.'.join(path_items)
    if '\\' in bot_name:
        bot_name = bot_name.split('\\')[-1]
    if not bot_name.startswith('ev') and not bot_name.startswith('m'):    
        bot_name, port = change_bot_name(bot_name, is_buying_bot)
    else:       
        port = find_port(bot_name)
    this_socket = ManagerClient(bot_name, tabs, accounts, port, is_buying_bot)
    this_socket.start()
    return this_socket