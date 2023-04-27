import pickle
from multiprocessing import Queue

import requests
import urllib3
from requests.exceptions import SSLError, ProxyError
from urllib3.exceptions import InsecureRequestWarning

from .telecore import TeleCore
from . import main_utils
from .vis import *
from .cores import BotCore

DEBUG_TELE_IDS = [454746771, 1128666119, 647298152]
with open('config.json') as f:
    settings = json.load(f)
ERRORS = ['500 Internal Server Error', '504 Gateway Time-out', '502 Bad Gateway', 'Сервис временно недоступен']


def load_proxies():
    source_path = main_utils.get_source_path()
    if os.path.exists('json\\proxies.json'):
        print(green('Personal proxies for this bot loaded'))
        proxies_json_path = 'json\\proxies.json'
    else:
        proxies_json_path = source_path + '\\proxies.json'
    with open(proxies_json_path, 'r') as proxiesjson:
        proxies = json.load(proxiesjson)
    return proxies


class PickleSaver(threading.Thread):
    def __init__(self):
        super().__init__()
        self.pickles_to_save = []
        #self.save_lock = threading.Lock()
    
    def put(self, fpath, data):
        self.pickles_to_save.append((fpath, data))
        
    def save(self):
        pickles = self.pickles_to_save
        self.pickles_to_save = []
        for fpath, data in pickles:
            with open(fpath, 'wb+') as f:
                pickle.dump(data, f)
        
    def run(self):
        while True:
            try:
                time.sleep(10)
                self.save()
            except:
                print(red('Error while saving pickles'))


class Account:
    tab_counter = 0
    if not os.path.exists('account_pickles'):
        os.mkdir('account_pickles')
    proxy_list = load_proxies()
    plen = len(proxy_list)
    
    save_thread = PickleSaver()
    save_thread.start()

    def __init__(self, login, password):
        super().__init__()
        self.session = requests.Session()
        self.login = login
        self.password = password
        Account.tab_counter += 1
        self.tab = Account.tab_counter
        self.file_path = f'account_pickles\\{self.login}_{self.password}.acc.pickle'
        self.file_path = self.file_path.replace('*', '')
        self.last_session = 0
        self.pickling = True
        
        self.load_on_init()
        
    def __str__(self):
        return f'[Account {self.login} {self.password} #{self.tab}]'
        
    def load_on_init(self):
        if os.path.exists(self.file_path):
            self.load()
            
    def change_ip(self):
        self.tab += 1
            
    def change_identity(self):
        self.tab += 1
        self.deauthorize()
        
    def get_proxy(self):
        i = (self.tab - 1) % self.plen
        proxy = self.proxy_list[i]
        return main_utils.parse_proxy(proxy)
        
    def proxy(self):
        i = (self.tab - 1) % self.plen
        proxy = self.proxy_list[i]
        _, host, port, _, _ = main_utils.parse_proxy(proxy)
        return f"{host}:{port}"
        
    def requests_proxies(self):
        ptype, host, port, user, pwd = self.get_proxy()
        proxies = {
            'http' : '%s://%s:%s@%s:%d' % (ptype, user, pwd, host, port),
            'https' : '%s://%s:%s@%s:%d' % (ptype, user, pwd, host, port)
        }
        return proxies
        
    def load(self):
        try:
            with open(self.file_path, 'rb') as f:
                self.session.cookies, self.last_session = pickle.load(f)
        except:
            print('Redumping pickle for', self.login)
            self.save()
            
    def save(self):
        if not self.pickling:
            return True
        data = [self.session.cookies, self.last_session]
        self.save_thread.put(self.file_path, data)
        
    def deauthorize(self):
        self.last_session = 0
        self.session = requests.Session()
        self.save()
            
    def get(self, *args, **kwargs):
        self.last_session = time.time()
        r = self.session.get(*args, **kwargs, proxies=self.requests_proxies())
        self.save()
        return r
            
    def post(self, *args, **kwargs):
        self.last_session = time.time()
        r = self.session.post(*args, **kwargs, proxies=self.requests_proxies())
        self.save()
        return r
            
    def put(self, *args, **kwargs):
        self.last_session = time.time()
        r = self.session.put(*args, **kwargs, proxies=self.requests_proxies())
        self.save()
        return r
            
    def head(self, *args, **kwargs):
        self.last_session = time.time()
        r = self.session.head(*args, **kwargs, proxies=self.requests_proxies())
        self.save()
        return r
        
    def delete(self, *args, **kwargs):
        self.last_session = time.time()
        r = self.session.delete(*args, **kwargs, proxies=self.requests_proxies())
        self.save()
        return r


class RushAccount(Account):

    def __init__(self, login, password):
        super().__init__(login, password)

    def get(self, *args, **kwargs):
        kwargs['verify'] = False
        while True:
            try:
                r = super().get(*args, **kwargs)
                for err in ERRORS:
                    if err in r.text:
                        raise ConnectionError
                else:
                    return r
            except ConnectionError:
                print('$', end='')
            except urllib3.HTTPSConnectionPool:
                print('%', end='')
            except SSLError:
                print('#', end='')
            except ProxyError:
                print('&', end='')

    def post(self, *args, **kwargs):
        kwargs['verify'] = False
        while True:
            try:
                r = super().post(*args, **kwargs)
                for err in ERRORS:
                    if err in r.text:
                        print('^', end='')
                        raise ConnectionError
                else:
                    return r
            except ConnectionError:
                print('$', end='')
            except urllib3.HTTPSConnectionPool:
                print('%', end='')
            except SSLError:
                print('#', end='')


class AccountsQueue(threading.Thread):
    def __init__(self, accounts_path, separator='\t', mix=False,
                 ignore_limit=False, reauthorize=False):
        super().__init__()
        self.accounts_path = accounts_path
        self.separator = separator
        self.mix = mix
        self.ignore_limit = ignore_limit
        self.reauthorize = reauthorize
        
        self.session_threads = settings['session_threads']
        session_time = settings['session_duration']
        self.session_time = session_time - 30
        self.inspect_time = session_time // 2
        self.check_for_inspect_time = session_time // 12
        
        self.user_agent = BotCore.user_agent
        self.ready = Queue()
        self.to_inspect = Queue()
        self.filled = False
        self.inspector_working = 0
        self.accounts_check = False
        self.mean_try_login = []
        self.bot_name = sys.argv[0]
        if ':\\' in self.bot_name:
            self.bot_name = self.bot_name.split('\\')[-1]
        
    def __str__(self):
        return f"({self.ready.qsize()}, {self.to_inspect.qsize()})"
        
    def first_fill_queue(self):
        with open(self.accounts_path, 'r', encoding='utf-8') as f:
            rows = []
            for row in f.read().split('\n'):
                if not row or row.startswith('--'):
                    continue
                if not self.separator in row:
                    raise RuntimeError(f'No separator in account line {row}')
                logpass = row.split(self.separator)
                rows.append(logpass)
        for i in range(len(rows)):
            if rows[i][-1].endswith('\r'):
                rows[i] = rows[i][:-1]
            
        parts = self.accounts_path.split('.')
        name = '.'.join(parts[:-1])
        extension = parts[-1]
        blacklist_path = f'{name}_blacklist.{extension}'
        
        if not os.path.exists(blacklist_path):
            with open(blacklist_path, 'w+') as f:
                f.write('')
        with open(blacklist_path, 'r') as f:
            black_rows = [row.split(self.separator) for row in f.read().split('\n')
                              if row and not row.startswith('--')]
        rows = [row for row in rows if row not in black_rows]
        
        if self.mix:
            random.shuffle(rows)
        if 'max_sessions' in settings and not self.ignore_limit:
            max_sessions = settings['max_sessions']
            print(green('MAX THREADS COUNT: ' + str(max_sessions)))
            rows = rows[:max_sessions]
            
        usual_args = [self.put, fpass, 'Sub', 1]
        aims = [[usual_args, {'args': row}, ', '.join(row)] for row in rows]
        results = pool(multi_try, aims, settings['session_threads'])
        bad_results = {item: results[item] for item in results if not results[item]}
        
        if bad_results:
            lprint('Ошибки авторизации:', color=Fore.RED)
            lp_dict(bad_results)
            print(red('--------'))
        else:
            print(green('Все сессии прогрузились!'))

        self.filled = True
        self.accounts_check = True
        if self.mean_try_login:
            mean = (sum(self.mean_try_login) / len(self.mean_try_login))
            print(green("Среднее кол-во попыток на вход: " + "%.1f" % mean))
        
    def is_filled(self):
        print(self.filled, self.to_inspect.qsize())
        return self.filled and not self.to_inspect.qsize()

    def put_very_old(self, account):
        account.pickling = False
        try:
            self.login(account)
        except Exception as exception:
            if self.is_permanently_banned(account):
                print('Permanently banned', account.login, account.password)
                self.add_to_blacklist(account)
            raise exception
        account.pickling = True
        account.save()
        if not self.first_check(account):
            print(yellow('First check returned False'))
            return False
            
        self.ready.put(account)
    
    def put_to_inspectation(self, account):
        self.to_inspect.put(account)
    
    def put_fresh(self, account):
        account.pickling = False
        if self.is_permanently_banned(account):
            print('Permanently banned', account.login, account.password)
            self.add_to_blacklist(account)
            return False
        account.pickling = True
        account.save()
            
        if not self.first_check(account):
            return False
            
        self.ready.put(account)
            
    def put(self, *args):
        if len(args) == 1:
            account = args[0]
        else:
            account = RushAccount(*args)
        time_elapsed = time.time() - account.last_session
        if self.reauthorize:
            account.change_identity()
        if (time_elapsed > self.session_time) or self.reauthorize: 
            self.put_very_old(account)
        elif time_elapsed > self.inspect_time:
            try:
                self.put_to_inspectation(account)
            except:
                self.put_very_old(account)
        else:
            self.put_fresh(account)
        print('.', end='')
            
    def qsize(self):
        return self.ready.qsize(), self.to_inspect.qsize()
            
    def get(self):
        account = self.ready.get()
        return account
        
    def first_check(self, account):
        pass
    
    def login(self, account):
        pass
        
    def is_logined(self, account):
        # Requests in this method should continue opened session
        pass
        
    def is_permanently_banned(self, account):
        return False
        
    def ban(self, account):
        return self.add_to_blacklist(account)
        
    def add_to_blacklist(self, account):
        parts = self.accounts_path.split('.')
        name = '.'.join(parts[:-1])
        extension = parts[-1]
        blacklist_path = f'{name}_blacklist.{extension}'
        black_row = f"{account.login}\t{account.password}\n"
        with open(blacklist_path, 'a') as f:
            f.write(black_row)

    def change(self, account):
        self.put(account)
        print(yellow('Account changed'))
        return self.get()
        
    def test(self):
        def test(time_test, account):
            try:
                self.login(account)
            except:
                print('Error logining')
            time.sleep(time_test)
            test_result = self.is_logined(account)
            lprint(f'Test result for {time_test} s: {test_result}')
            
        with open(self.accounts_path, 'r') as f:
            logpasses = [row.split(self.separator) for row in f.read().split('\n')]
        accounts = [RushAccount(*logpass) for logpass in logpasses]
        time_tests = [10, 290, 590, 890, 1190, 1790, 3590, 7190, 10790]
        for time_test, account in zip(time_tests, accounts):
            threading.Thread(target=test, args=(time_test, account,)).start()
        
    def run_inspector(self):
        last_time_mes = 0

        def inspect(account):
            self.inspector_working += 1
            account.pickling = False
            if not self.is_logined(account):
                print('While inspecting, not logined', account.login, account.password)
                account = RushAccount(account.login, account.password)
                try:
                    self.login(account)
                except:
                    print(red(f'Error logining while inspecting, {account}'))
                    time.sleep(30)
                    self.put_to_inspectation(account)
                    self.inspector_working -= 1
                    return False
                if self.is_permanently_banned(account):
                    print(red(f'Permanently banned {account}'))
                    self.add_to_blacklist(account)
                    self.inspector_working -= 1
                    return False
            account.pickling = True
            account.save()
            if not self.first_check(account):
                self.inspector_working -= 1
                return False
            self.ready.put(account)
            self.inspector_working -= 1

        def on_cancel():
            self.inspector_working -= 1

        while True:
            account = self.to_inspect.get()
            if self.ready.qsize() == 0 and time.time() - last_time_mes > 300 and self.accounts_check:
                lprint('авторайз обнаружил понос в аккаунтах')
                TeleCore.send_message(f'Вылетели ВСЕ аккаунты!!!!!!! --- {self.bot_name}', DEBUG_TELE_IDS)
                last_time_mes = time.time()
            while True:
                if self.inspector_working >= self.session_threads:
                    time.sleep(1)
                else:
                    args = (inspect, on_cancel, 'Sub', 1,)
                    kwargs = {'args': [account]}
                    threading.Thread(target=multi_try, args=args, kwargs=kwargs).start()
                    break
        
    def run(self):
        threading.Thread(target=self.run_inspector).start()
        self.first_fill_queue()
        while True:
            time.sleep(self.check_for_inspect_time)
            while not self.ready.empty():
                account = self.ready.get()
                time_elapsed = time.time() - account.last_session
                if time_elapsed > self.inspect_time:
                    self.to_inspect.put(account)
                else:
                    self.ready.put(account)


urllib3.disable_warnings(InsecureRequestWarning)
