import os
import re
import sys
import time
import socks
import ftplib
import socket
import shutil
import threading

path = os.path.dirname(os.path.abspath(__file__))
s_path = path.split('\\')
s_path.pop()
root_path = '\\'.join(s_path)
sys.path.insert(0, root_path + '\\[MySources]')

from vis import *
from colorama import Fore, Back

default_fore = Fore.BLACK
default_back = Back.CYAN

#from PyQt5 import QtWidgets, QtGui, QtCore, uic
#from qt_forms import Ui_MainWindow

"""class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        with open(r"sources\darkorange.stylesheet","r") as fh:
            self.setStyleSheet(fh.read())
        entries = ['one','two', 'three']

        model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(model)

        for i in entries:
            item = QtGui.QStandardItem(i)
            model.appendRow(item)"""
            
class Connection:
    def __init__(self, conn, bot_name):
        self.conn = conn
        self.bot_name = bot_name

    def read(self):
        data = self.conn.recv(1024)
        return self.bot_name + ': ' + data.decode('utf-8')

    def send(self, mes):
        self.conn.send(mes.encode('utf-8'))

class RuntimeController(threading.Thread):
    def __init__(self, conns, port):
        threading.Thread.__init__(self)
        self.port = port
        self.conns = conns
        
    def run_bot(self, bot_name):
        link_name = f'{root_path}\\{bot_name}.lnk'
        os.startfile(link_name)
        
    def run(self):
        def load_config():
            with open(f'{root_path}\\[MySources]\\[config].json', 'r') as f:
                payload = f.read()
            lines = payload.split('\n')
            lines = [line for line in lines if '#' not in line[:4]]
            last_line = lines[-2]
            if last_line[-1] == ',':
                without_comma = last_line[:-1]
                lines[-2] = without_comma
            payload = '\n'.join(lines)
            config = json.loads(payload)
            return config
        def check_if_alive():
            try:
                self.conns[bot_name].send('is_alive')
                self.conns[bot_name].read()
            except socket.error:
                del self.conns[bot_name]
                print(bot_name + ' aborted')
            except KeyError as error:
                self.run_bot(bot_name)
                time.sleep(3)
        def check_if_still_in_whitelist(bot_name):
            if bot_name in bot_names:
                return True
            try:
                self.conns[bot_name].send('shutdown')
                print(bot_name + ': shutted down - not in whitelist')
            except:
                pass
                
        while True:
            try:
                with open(f'{root_path}\\[MySources]\\ChrTab.txt', 'w') as f:
                    f.write('10')
                break
            except:
                print('Error writing to ChrTab.txt')
                time.sleep(1)
        while True:
            config = load_config()
            
            now = time.time()
            for bot_time, bot_name, manager_port in config:
                if manager_port != self.port:
                    continue
                if now < bot_time:
                    continue
                check_if_alive()
                
            bot_names = [line[1] for line in config]
            for bot_name in self.conns:
                check_if_still_in_whitelist(bot_name)
                
            time.sleep(5)
            
class DataSynchronizer(threading.Thread):
    def __init__(self,
                host,
                user,
                pwd,
                local_path,
                delay=60,
                del_priority='in',
                time_zone_inc=0,
                filters=[],
                close_at_end=False):
        threading.Thread.__init__(self)
        self.ftp_connection = [host, user, pwd]
        self.ftp = start_ftp(host, user, pwd)
        self.locker = True
        self.local_path = local_path
        self.delay = delay
        self.del_priority = del_priority
        self.time_zone_inc = time_zone_inc
        self.cwd = []
        self.cwd_abs = ''
        self.filters = filters
        self.close_at_end = close_at_end
        
    def __del__(self):
        self.ftp.quit()
        
    def download_file(self, file_name):
        rprint('downloading ' + self.cwd + file_name)
        try:
            with open(self.local_path + '\\' + self.cwd + file_name, 'wb') as f:
                self.ftp.retrbinary('RETR ' + '\\' + self.cwd + file_name, f.write)
        except:
            rprint('Error downloading ' + self.cwd + file_name)
            
    def upload_file(self, file_name):
        rprint('uploading ' + self.cwd + file_name)
        try:
            with open(self.local_path + '\\' + self.cwd + file_name, 'rb') as f:
                self.ftp.storbinary('STOR ' + '\\' + self.cwd + file_name, f)
        except:
            rprint('Error uploading ' + self.cwd + file_name)
        
    def remove_local_file(self, file_name):
        try:
            os.remove(self.local_path + '\\' + self.cwd + file_name)
        except:
            rprint('Error removing ' + self.cwd + file_name)
        
    def remove_remote_file(self, file_name):
        try:
            self.ftp.delete('\\' + self.cwd + file_name)
        except:
            rprint('Error removing ' + self.cwd + file_name)
        
    def create_local_dir(self, dir_name):
        try:
            os.mkdir(self.local_path + '\\' + self.cwd + dir_name)
        except:
            rprint('Error creating ' + self.cwd + dir_name)
        self.local_dirs.append(self.cwd + dir_name)
        
    def remove_local_dir(self, dir_name):
        try:
            shutil.rmtree(self.local_path + '\\' + self.cwd + dir_name, ignore_errors=True)
        except:
            rprint('Error removing ' + self.cwd + file_name)
        self.local_dirs = [dir for dir in self.local_dirs if not dir.startswith(self.cwd + dir_name)]
        
    def create_remote_dir(self, dir_name):
        try:
            self.ftp.mkd('\\' + self.cwd + dir_name)
        except:
            rprint('Error creating ' + self.cwd + dir_name)
        self.remote_dirs.append(self.cwd + dir_name)
    
    def remove_remote_dir(self, dir_name):
        cwd = self.cwd
        def del_dir(dir_):
            rprint('deleting ', dir_)
            self.cwd_abs = dir_
            self.cwd = self.cwd_abs + '\\' if self.cwd_abs else ''
            self.ftp.cwd('\\' + self.cwd_abs)
            r_dirs, r_files = self.get_remote_list(filters=False)
            for file in r_files:
                self.ftp.delete('\\' + dir_ + '\\' + file[1])
            for dirr_ in r_dirs:
                del_dir(dir_ + '\\' + dirr_)
            self.ftp.rmd('\\' + dir_)
        first_dir = cwd + dir_name
        del_dir(first_dir.replace('\\\\', '\\'))
        self.cwd_abs = cwd
        self.cwd = self.cwd_abs + '\\' if self.cwd_abs else ''
        self.ftp.cwd('\\' + self.cwd_abs)
        self.remote_dirs = [dir for dir in self.remote_dirs if not dir.startswith(self.cwd + dir_name)]
        
    def get_remote_list(self, filters=True):
        def get_seconds(us_time):
            left, right = us_time.split(' ')
            m, d, y = left.split('-')
            m = int(m)
            d = int(d)
            y = 2000 + int(y)
            clock = right[:5]
            am_pm = right[-2:]
            h, min = clock.split(':')
            h = int(h)
            min = int(min)
            if (h == '12') and (am_pm == 'AM'):
                h = 0
            elif (h == '12') and (am_pm == 'PM'):
                h = 12
            elif am_pm == 'PM':
                h += 12
            structed = (y, m, d, h, min, 0, 0, 0 ,0)
            seconds = time.mktime(structed)
            seconds += self.time_zone_inc * 3600
            return seconds
            
        def store(line):
            while '  ' in line:
                line = line.replace('  ', ' ')
            day, time_, type_, file_name = line.split(' ', 3)
            date = day + ' ' + time_
            if type_ == '<DIR>':
                server_dirs.append(file_name)
            else:
                server_files.append([get_seconds(date), file_name])
        server_files = []
        server_dirs = []
        self.ftp.retrlines('LIST', callback=store)
        if not filters:
            return server_dirs, server_files
        server_dirs_filtered = []
        for item in server_dirs:
            for filter in self.filters[0:1]:
                if re.search(filter, item):
                    break
            else:
                server_dirs_filtered.append(item)
        server_files_filtered = []
        for mtime, item in server_files:
            for filter in self.filters:
                if re.search(filter, item):
                    break
            else:
                server_files_filtered.append([mtime, item])
        return server_dirs_filtered, server_files_filtered
        
    def get_all_local_list(self):
        def get_seconds(file_path):
            return os.path.getmtime(file_path)
            
        local_dirs = []
        local_files = []
        for top, dirs, files in os.walk(self.local_path):
            rel_top = top.split(self.local_path)[1]
            if rel_top:
                rel_top += '\\'
                if rel_top[0] == '\\':
                    rel_top = rel_top[1:]
            local_dirs.extend([f'{rel_top}{dir}' for dir in dirs])
            local_files.extend([[get_seconds(f'{top}\\{file}'), f'{rel_top}{file}'] for file in files])
        local_dirs_ = []
        for item in local_dirs:
            for filter in self.filters[0:1]:
                if re.search(filter, item):
                    break
            else:
                local_dirs_.append(item)
        local_files_ = []
        for mtime, item in local_files:
            for filter in self.filters:
                if re.search(filter, item):
                    break
            else:
                local_files_.append([mtime, item])
        return local_dirs_, local_files_
        
    def get_local_cwd_list(self):
        def get_seconds(file_path):
            return os.path.getmtime(file_path)
            
        local_dirs = []
        local_files = []
        for top, dirs, files in os.walk(self.local_path + '\\' + self.cwd_abs):
            rel_top = top.split(self.local_path + '\\' + self.cwd_abs)[1]
            if rel_top:
                rel_top += '\\'
                if rel_top[0] == '\\':
                    rel_top = rel_top[1:]
            local_dirs.extend([f'{rel_top}{dir}' for dir in dirs])
            local_files.extend([[get_seconds(f'{top}\\{file}'), f'{rel_top}{file}'] for file in files])
            break
        local_dirs_ = []
        for item in local_dirs:
            for filter in self.filters[0:1]:
                if re.search(filter, item):
                    break
            else:
                local_dirs_.append(item)
        local_files_ = []
        for mtime, item in local_files:
            for filter in self.filters:
                if re.search(filter, item):
                    break
            else:
                local_files_.append([mtime, item])
        return local_dirs_, local_files_
        
    def get_local_list(self):
        local_dirs = []
        local_files = []
        for item in self.local_dirs:
            if not((item.startswith(self.cwd_abs + '\\')) or (not self.cwd_abs)):
                continue
            if self.cwd_abs:
                parts = item.split(self.cwd_abs + '\\', 1)
                rel_path = parts[1]
            else:
                rel_path = item
            if '\\' not in rel_path:
                local_dirs.append(rel_path)
        for item in self.local_files:
            mdate, file_name = item
            if not((file_name.startswith(self.cwd_abs + '\\')) or (not self.cwd_abs)):
                continue
            if self.cwd_abs:
                parts = file_name.split(self.cwd_abs + '\\', 1)
                rel_path = parts[1]
            else:
                rel_path = file_name
            if '\\' not in rel_path:
                to_append = [mdate, rel_path]
                local_files.append(to_append)
        return local_dirs, local_files
        
    def get_both_lists(self, dir_):
        self.cwd_abs = dir_
        self.cwd = self.cwd_abs + '\\' if self.cwd_abs else ''
        self.ftp.cwd('\\' + self.cwd_abs)
        local_dirs, local_files = self.get_local_list()
        def to_try():
            self.got_remote_dirs, self.got_remote_files = self.get_remote_list()
        def to_except():
            rprint('Restarting connections')
            self.ftp = start_ftp(*self.ftp_connection)
            self.ftp.cwd('\\' + self.cwd_abs)
        multi_try(to_try, to_except, 'RemoteList', 3)
        return local_dirs, local_files, self.got_remote_dirs, self.got_remote_files
        
    def walk(self):
        def differences_(left, right):
            dict1 = {file_name: date for date, file_name in left}
            dict2 = {file_name: date for date, file_name in right}
            dif1_dict = {elem: dict1[elem] for elem in dict1 if elem not in dict2}
            dif2_dict = {elem: dict2[elem] for elem in dict2 if elem not in dict1}
            dif1 = [[dif1_dict[elem], elem] for elem in dif1_dict]
            dif2 = [[dif2_dict[elem], elem] for elem in dif2_dict]
            intersection = list(set(dict1.keys()) & set(dict2.keys()))
            dif1_newer = []
            for elem in intersection:
                elem_path = self.cwd + elem
                if elem_path in self.config:
                    bool_ = dict1[elem] > self.config[elem_path][0]
                else:
                    bool_ = dict1[elem] > dict2[elem]
                if bool_:
                    to_append = [None, elem]
                    dif1_newer.append(to_append)
            dif2_newer = []
            for elem in intersection:
                elem_path = self.cwd + elem
                if elem_path in self.config:
                    bool_ = dict2[elem] > self.config[elem_path][1]
                else:
                    bool_ = dict2[elem] > dict1[elem]
                if bool_:
                    to_append = [None, elem]
                    dif2_newer.append(to_append)
            return dif1, dif1_newer, dif2_newer, dif2, []
        def compare_and_transfer(dir_):
            l_dirs, l_files, r_dirs, r_files = self.get_both_lists(dir_)
            dirs_to_add = [self.cwd + dir for dir in r_dirs]
            self.remote_dirs += dirs_to_add
            
            # FILES
            if self.del_priority == 'in':
                to_up, to_up_, to_down_, to_del, to_down = differences_(l_files, r_files)
                for elem in to_del:
                    file_name = elem[1]
                    self.remove_remote_file(file_name)
            elif self.del_priority == 'out':
                to_del, to_up_, to_down_, to_down, to_up = differences_(l_files, r_files)
                for elem in to_del:
                    file_name = elem[1]
                    self.remove_local_file(file_name)
            else:
                to_up, to_up_, to_down_, to_down, to_del = differences_(l_files, r_files)
                for elem in to_del:
                    file_name = elem[1]
                    self.remove_local_file(file_name)
            for elem in to_up + to_up_:
                self.upload_file(elem[1])
            for elem in to_down + to_down_:
                self.download_file(elem[1])
            if to_up or to_up_ or to_down_ or to_down or to_del:
                l_dirs, l_files = self.get_local_cwd_list()
                r_dirs, r_files = self.get_remote_list()
                l_dict = {self.cwd + file_name: date for date, file_name in l_files}
                r_dict = {self.cwd + file_name: date for date, file_name in r_files}
                for key in l_dict.keys():
                    l_time = l_dict[key]
                    r_time = r_dict[key]
                    self.config[key] = [l_time, r_time]
            # DIRS
            to_up = []
            to_down = []
            if self.del_priority == 'in':
                to_up, _, to_del = differences(l_dirs, r_dirs)
                for elem in to_del:
                    self.remove_remote_dir(elem)
            elif self.del_priority == 'out':
                to_del, _, to_down = differences(l_dirs, r_dirs)
                for elem in to_del:
                    self.remove_local_dir(elem)
            else:
                to_up, _, to_down = differences(l_dirs, r_dirs)
            for elem in to_up:
                self.create_remote_dir(elem)
            for elem in to_down:
                self.create_local_dir(elem)
            
        self.local_dirs, self.local_files = self.get_all_local_list()
        self.local_dirs += ['']
        self.remote_dirs = ['']
        with open('synchro_config.txt', 'r+') as f:
            self.config = json.load(f)
        
        while self.remote_dirs:
            got_dir = self.remote_dirs.pop()
            if self.del_priority != 'out':
                print(got_dir)
            #try:
            self.local_dirs.remove(got_dir)
            #except:
            #    print('Error removing from list: ', got_dir)
            compare_and_transfer(got_dir)
        
        with open('synchro_config.txt', 'w') as f:
            json.dump(self.config, f)
        
        
    def run(self):
        while True:
            def to_try():
                start_time = time.time()
                self.walk()
                elapsed = int(time.time() - start_time)
                rprint(f'Completed in {elapsed} sec')
            def to_except():
                rprint('Error while synchronizing data')
                self.ftp = start_ftp(*self.ftp_connection)
                print('Entering in \\' + self.cwd_abs)
                self.ftp.cwd('\\' + self.cwd_abs)
            multi_try(to_try, to_except, 'Main', 1, True)
            if self.close_at_end:
                os._exit(0)
            for _ in range(int(self.delay)):
                time.sleep(1)
                if not self.locker:
                    print('Instant synchronize')
                    self.locker = True
                    break
            
class BotSynchronizer(DataSynchronizer):
    def __init__(self, delay=30, time_zone_inc=0, del_priority='out', close_at_end=False):
        local_path = root_path
        filters = [
            '.acc.pickle',
            '__pycache__',
            'captcha_(.*)[.]png',
            '.pyc',
            'chromedriver.exe.',
            'debug.log',
            'debug.txt',
            'ext_(.*)[.]zip',
            'log(.*)[.]txt',
            'desktop.ini',
            'synchro_config.txt',
            'ChrTab.txt',
            '.rar', ###############
            '.zip' ################
        ]
        super().__init__('185.203.119.33',
            'Administrator',
            'aE5zAlT03ZGxmrJ!',
            local_path=local_path,
            delay=delay,
            del_priority=del_priority,
            time_zone_inc=time_zone_inc,
            filters=filters,
            close_at_end=close_at_end)
        if sys.getwindowsversion().product_type != 3:
            with open('system_proxy.json') as f:
                p_host, p_port, p_user, p_pwd = json.load(f)
            socks.set_default_proxy(socks.HTTP, 
                    p_host, 
                    p_port, 
                    username=p_user,
                    password=p_pwd
            )
            socket.socket = socks.socksocket
            print(green('SYSTEM PROXY IS SET UP'))
        
def start_ftp(host, user, pwd):
    ftp = ftplib.FTP(host)
    ftp.login(user=user, passwd=pwd)
    ftp.makepasv()
    ftp.encoding = 'utf-8'
    ftp.sendcmd('OPTS UTF8 ON')
    return ftp
        
def rprint(*mes):
    full_mes = ' '.join(mes)
    print(colorize(full_mes, Fore.RED))
            
def start_manager(port):
    def grab_enter():
        while True:
            _ = input()
            synchronizer_thread.locker = False
    #app = QtWidgets.QApplication([])
    #application = mywindow()
    #application.show()

    os.system("cls")
    os.system('color b0')
    connections = {}
    controller_thread = RuntimeController(connections, port)
    controller_thread.start()
    if port != 9091:
        synchronizer_thread = BotSynchronizer()
        synchronizer_thread.start()
        Threadize(grab_enter)

    from get_ip import get_local_ip
    server = socket.socket()
    server.bind((get_local_ip(), port))
    server.listen(0)
    while True:
        conn, addr = server.accept()
        data = conn.recv(1024)
        bot_name = data.decode('utf-8')
        print(bot_name + ' connected')
        connection = Connection(conn, bot_name)
        connections[bot_name] = connection
    #sys.exit(app.exec())