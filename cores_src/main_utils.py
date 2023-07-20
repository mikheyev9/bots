import os
import json
import random

import requests
from socketserver import *

from .vis import red

python_encodings = {
    "ascii", "big5", "big5hkscs", "cp037", "cp273", 
    "cp424", "cp437", "cp500", "cp720", 
    "cp737", "cp775", "cp850", "cp852", 
    "cp855", "cp856", "cp857", "cp858", 
    "cp860", "cp861", "cp862", "cp863", 
    "cp864", "cp865", "cp866", "cp869", 
    "cp874", "cp875", "cp932", "cp949", 
    "cp950", "cp1006", "cp1026", "cp1125",
    "cp1140", "cp1250", "cp1251", "cp1252", 
    "cp1253", "cp1254", "cp1255", "cp1256", 
    "cp1257", "cp1258", "euc_jp", "euc_jis_2004", 
    "euc_jisx0213", "euc_kr", "gb2312", "gbk", 
    "gb18030", "hz", "iso2022_jp", "iso2022_jp_1", 
    "iso2022_jp_2", "iso2022_jp_2004", 
    "iso2022_jp_3", "iso2022_jp_ext", 
    "iso2022_kr", "latin_1", "iso8859_2", "iso8859_3", 
    "iso8859_4", "iso8859_5", "iso8859_6", "iso8859_7", 
    "iso8859_8", "iso8859_9", "iso8859_10", "iso8859_11", 
    "iso8859_13", "iso8859_14", "iso8859_15", "iso8859_16", 
    "johab", "koi8_r", "koi8_t", "koi8_u", 
    "kz1048", "mac_cyrillic", "mac_greek", "mac_iceland", 
    "mac_latin2", "mac_roman", "mac_turkish", "ptcp154", 
    "shift_jis", "shift_jis_2004", "shift_jisx0213", "utf_32", 
    "utf_32_be", "utf_32_le", "utf_16", "utf_16_be", 
    "utf_16_le", "utf_7", "utf_8", "utf_8_sig"
}


class MyTCPHandler(StreamRequestHandler):
    """
    process_message(self, to_load) -
        loads processed message with JSON
    TCPServer((ip, port), MyTCPHandler).serve_forever() -
        to handle messages
    """
    buffer = ''
    
    def process_buffer(self):
        data_packs = self.buffer.split(chr(2))
        self.buffer = data_packs.pop()
        for data_pack in data_packs:
            to_load = json.loads(data_pack)
            self.process_message(to_load)
    
    #доступны несколько атрибутов: запрос доступен как self.request,
    #адрес как self.client_address, экземпляр сервера как self.server
    def handle(self):
        try:
            data = self.request.recv(1024)
            #print(f'first {data} {self.server.server_address}')
        except Exception as error:
            print('Error receiving data by TCP handler: ' + str(error))
            return True
        self.buffer += bytes.decode(data)
        while b'\x02' not in data:
            data = self.request.recv(1024)
            #print(f'first {data} {self.server.server_address}')
            self.buffer += bytes.decode(data)
        try:
            self.process_buffer()
        except:
            print('Error processing message buffer!')
            self.buffer = ''

    def process_message(self, to_load):
        pass


class ProxySession(requests.Session):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    def get(self, *args, **kwargs):
        kwargs['proxies'] = self.bot.requests_proxies()
        return super().get(*args, **kwargs)
    
    def post(self, *args, **kwargs):
        kwargs['proxies'] = self.bot.requests_proxies()
        return super().post(*args, **kwargs)
        
    def put(self, *args, **kwargs):
        kwargs['proxies'] = self.bot.requests_proxies()
        return super().put(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        kwargs['proxies'] = self.bot.requests_proxies()
        return super().delete(*args, **kwargs)
    
            
def get_source_path():
    path = os.path.dirname(os.path.abspath(__file__))
    s_path = path.split('\\')[:-1]
    return '\\'.join(s_path) + '\\cores_src\\'


def parse_proxy(proxy):
    proxy_type = 'http'
    if type(proxy).__name__ == 'str':
        proxy_user = ''
        proxy_pass = ''
        if r'://' in proxy:
            proxy_type, proxy = proxy.split(r'://')
        if '@' in proxy:
            proxy, logpass = proxy.split('@')
            proxy_user, proxy_pass = logpass.split(':')
        spl_proxy = proxy.split(':')
        proxy_host = spl_proxy[0]
        proxy_port = int(spl_proxy[1])
    elif len(proxy) == 5:
        proxy_type, proxy_host, proxy_port, proxy_user, proxy_pass = proxy
    elif len(proxy) == 4:
        proxy_host, proxy_port, proxy_user, proxy_pass = proxy
    elif len(proxy) == 3:
        proxy_type, proxy_host, proxy_port = proxy
        proxy_user = ''
        proxy_pass = ''
    elif len(proxy) == 2:
        proxy_host, proxy_port = proxy
        proxy_user = ''
        proxy_pass = ''
    else:
        print('WTF: proxies.json')
        return None
    return proxy_type, proxy_host, proxy_port, proxy_user, proxy_pass
    

def parse_gmail(mail):
    bits = len(mail) - 1
    pointer = 0
    for i in range(bits):
        pointer += 1
        bool = random.randint(0, 1)
        if bool:
            mail = mail[:pointer] + '.' + mail[pointer:]
            pointer += 1
    mail += '@gmail.com'
    return mail


def uni_format_str(str_, mode):
    if mode == 0:
        str_ = str_.replace('"', '[d_q]')

        str_ = str_.replace('\\u', '[s_u]')  # Маскируем важные \ чтоб их не удалить
        str_ = str_.replace('\\', '[b_s]')
        str_ = str_.replace('[s_u]', '\\u')  # Убираем маскировку`
    else:
        str_ = str_.replace('[d_q]', '"')
        str_ = str_.replace('[b_s]', '\\')

    return str_


def unicode_fix(unicode_str):
    uni_str = uni_format_str(unicode_str, 0)
    dict_str = '{"str": "' + uni_str + '"}'

    try:
        json_dict = json.loads(dict_str, strict=False)
    except:
        print(red('unicode_fix fail!'))
        return unicode_str

    json_dict['str'] = uni_format_str(json_dict['str'], 1)
    return json_dict['str']


def decode(encoded):
    for encoding in python_encodings:
        try:
            print(encoding.rjust(15) + ' -> ' + encoded.decode(encoding))
        except:
            print(encoding.rjust(15) + ' -> ERROR DECODING (NO CHARMAP)')


#def unicode_fix(unicode_str):
#    uni_str = unicode_str.replace('"', '[d_q]')
#    dict_str = '{"str": "' + uni_str + '"}'
#    
#    try:
#        json_dict = json.loads(dict_str) #strict=False izuchit
#    except:
#        print(red('unicode_fix() fail: ' + unicode_str))
#        return unicode_str
#    
#    json_dict['str'] = json_dict['str'].replace('[d_q]', '"')
#    return json_dict['str']
