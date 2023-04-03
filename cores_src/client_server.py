import json
import time
import platform
import threading

from multiprocessing import Queue
from socketserver import *
from socket import *

server = True if 'server' in platform.platform().lower() else False


def process_item(item):
    print('REDEFINE process_item', item)


class ServerHandler(StreamRequestHandler):
    buffer = ''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    #доступны несколько атрибутов: запрос доступен как self.request,
    #адрес как self.client_address, экземпляр сервера как self.server
    def handle(self):
        data = self.request.recv(1024)
        self.buffer += bytes.decode(data)
        while b'\x02' not in data:
            data = self.request.recv(1024)
            self.buffer += bytes.decode(data)
        #try:
        self.process_buffer()
        #except:
        #    print('Error processing message buffer!')
        #    time.sleep(0.1)
        #    self.buffer = ''
            
    def process_buffer(self):
        data_packs = self.buffer.split(chr(2))
        self.buffer = data_packs.pop()
        for data_pack in data_packs:
            to_load = json.loads(data_pack)
            for item in to_load:
                process_item(item)
        
class Server(threading.Thread):
    """
    Example:
    
    server = Server(ip, port)
    --redefine process_item(item) - client_server.process_item = process_item--
    server.start()
    """
    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip if server else 'localhost'
        self.port = port
        
    def run(self):
        TCPServer((self.ip, self.port), ServerHandler).serve_forever()
        
class Client(threading.Thread):
    """
    Example:
    
    client = Client(ip, port)
    client.send_message('Hello, world!')
    """
    
    def __init__(self, ip, port):
        super().__init__()
        self.q = Queue()
        self.ip = ip if server else 'localhost'
        self.port = port
        self.start()
        
    def send_message(self, item):
        self.q.put(item)
        
    def send_to_server(self, data):
        tcp_socket = socket(AF_INET, SOCK_STREAM)
        tcp_socket.connect((self.ip, self.port))

        data = str.encode(data)
        tcp_socket.send(data)
        response = tcp_socket.recv(1024)
        
        tcp_socket.close()
        
    def on_error(self, error_text):
        print(error_text)
        
    def run(self):
        while True:
            item = self.q.get()
            to_send = [item]
            time.sleep(0.01)
            while not self.q.empty():
                item = self.q.get()
                to_send.append(item)
            data = json.dumps(to_send) + chr(2)
            try:
                self.send_to_server(data)
            except Exception as error:
                self.on_error(str(error))


if __name__ == '__main__':
    server = Server('localhost', 9104)
    def process_item(item):
        print("NEWEST ONE, SHIT", item)
    process_item = process_item
    server.start()
    client = Client('localhost', 9104)
    client.send_message('Test chlenoglazik')
    client.send_message('Test chlenoglazik')
    client.send_message('Test chlenoglazik')
    client.send_message('Test chlenoglazik')
    client.send_message('Test chlenoglazik')
