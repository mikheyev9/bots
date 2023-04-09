import platform
from socket import *
from queue import Queue

import telebot

from . import main_utils
from .vis import *


try:
    tele_profiles_path = main_utils.get_source_path() + '\\tele_profiles.json'
    with open(tele_profiles_path, 'r') as tele_profiles_json:
        TELE_PROFILES = json.load(tele_profiles_json)
except:
    tele_profiles_path = main_utils.get_source_path() + 'tele_profiles.json'
    with open(tele_profiles_path, 'r') as tele_profiles_json:
        TELE_PROFILES = json.load(tele_profiles_json)


def start_telebot(telegram_key, pnum):
    bot = telebot.TeleBot(telegram_key)
    try:
        proxies_json_path = main_utils.get_source_path() + '\\proxies.json'
        with open(proxies_json_path, 'r') as proxiesjson:
            proxies = json.load(proxiesjson)
    except:
        proxies_json_path = main_utils.get_source_path() + 'proxies.json'
        with open(proxies_json_path, 'r') as proxiesjson:
            proxies = json.load(proxiesjson)
    p_type, p_host, p_port, p_user, p_pass = main_utils.parse_proxy(proxies[pnum])
    if pnum:
        telebot.apihelper.proxy = {'https':f'{p_type}://{p_user}:{p_pass}@{p_host}:{p_port}'}
    return bot


class TeleCore(threading.Thread):
    server = True
    q = Queue()

    def __init__(self):
        super().__init__()

    @staticmethod
    def send_message(mes, tele_ids):
        TeleCore.q.put([mes, tele_ids])
        
    def send_telegram_manually(self, mes, tele_ids):
        print('Notification server is offline! Sending manually...')
        
        mes_tele_ids = [tele_id for tele_id in tele_ids if tele_id not in [454746771, 647298152]]
        if mes_tele_ids == []:
            profiles = ''
        else:
            profiles = '\n['
            for mes_tele_id in mes_tele_ids:
                is_written = False
                for profile, profile_data in TELE_PROFILES.items():
                    if mes_tele_id == profile_data[0]:
                        profiles += profile + ', '
                        is_written = True
                
                if not is_written:
                    profiles += str(mes_tele_id) + ', '
            profiles = profiles[:-2] + ']'
        
        others_mes = mes
        our_mes = mes + profiles
        
        for tele_id in tele_ids:
            if tele_id in [454746771, 647298152]:
                mes = our_mes #
            else:
                mes = others_mes #
            try:
                self.bot.send_message(tele_id, mes)
            except Exception as error:
                if 'Forbidden: bot was blocked by the user' in str(error):
                    print(red(str(tele_id) + ' blocked the bot'))
                elif 'chat not found' in str(error):
                    print(red(str(tele_id) + ' not started chat with a bot'))
                else:
                    raise RuntimeError('TELEGRAM ERROR ' + str(error))
        
    def send_to_server(self, data):
        tcp_socket = socket(AF_INET, SOCK_STREAM)
        if self.server:
            tcp_socket.connect(('185.203.119.33', 9105))
        else:
            tcp_socket.connect(('localhost', 9105))

        data = str.encode(data)
        tcp_socket.send(data)
        response = tcp_socket.recv(1024)
        
        tcp_socket.close()
        
    def run(self):
        self.bot = start_telebot('6002068146:AAHx8JmyW3QhhFK5hhdFIvTXs3XFlsWNraw', -3)
        while True:
            to_send = []
            while not self.q.empty():
                mes_and_tele_ids = self.q.get()
                if mes_and_tele_ids[1] == [454746771, 647298152]:
                    mes_and_tele_ids[0] = '[Debug mode]\n' + mes_and_tele_ids[0]
                to_send.append(mes_and_tele_ids)
            data = json.dumps(to_send) + chr(2)
            try:
                self.send_to_server(data)
            except:
                for mes_and_tele_ids in to_send:
                    self.send_telegram_manually(*mes_and_tele_ids)
                    time.sleep(0.1)


class BillingCore(threading.Thread):
    server = True if 'server' in platform.platform().lower() else False
    q = Queue()

    def __init__(self):
        super().__init__()
        
    def send_message(mes, tele_ids):
        BillingCore.q.put([mes, tele_ids])
        
    def send_telegram_manually(self, mes, tele_ids):
        print('Notification server is offline! Sending manually...')
        
        mes_tele_ids = [tele_id for tele_id in tele_ids if tele_id not in [454746771, 647298152]]
        if mes_tele_ids == []:
            profiles = ''
        else:
            profiles = '\n['
            for mes_tele_id in mes_tele_ids:
                is_written = False
                for profile, profile_data in TELE_PROFILES.items():
                    if mes_tele_id == profile_data[0]:
                        profiles += profile + ', '
                        is_written = True
                    
                if not is_written:
                    profiles += str(mes_tele_id) + ', '
            profiles = profiles[:-2] + ']'
        
        others_mes = mes
        our_mes = mes + profiles
        
        for tele_id in tele_ids:
            if tele_id in [454746771, 647298152]:
                mes = our_mes
            else:
                mes = others_mes
            try:
                self.bot.send_message(tele_id, mes)
            except Exception as error:
                if 'Forbidden: bot was blocked by the user' in str(error):
                    print(red(str(tele_id) + ' blocked the bot'))
                elif 'chat not found' in str(error):
                    print(red(str(tele_id) + ' not started chat with a bot'))
                else:
                    TeleCore.send_message(mes, tele_ids)
                    break
        
    def run(self):
        self.bot = start_telebot('5741231744:AAGHiVougv4uoRia5I_behO9r1oMj1NEMI8', -4)
        while True:
            to_send = []
            while not self.q.empty():
                mes_and_tele_ids = self.q.get()
                if mes_and_tele_ids[1] == [454746771, 647298152]:
                    mes_and_tele_ids[0] = '[Debug mode]\n' + mes_and_tele_ids[0]
                to_send.append(mes_and_tele_ids)
            
            for mes_and_tele_ids in to_send:
                self.send_telegram_manually(*mes_and_tele_ids)
                time.sleep(0.1)


if __name__ == '__main__':
    TeleCore().start()
    for i in range(15):
        test_string = ''.join(str(i % 10) for i in range(random.randint(10, 60)))
        TeleCore.send_message(test_string, [454746771])