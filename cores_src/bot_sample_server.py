from multiprocessing import Queue

from .cores import *
from .vis import *
from . import bot_socket
from .default_config import check_config
from .ban_rules import BanRules

with open('config.json') as f:
    settings = json.load(f)
    check_config(settings)
with open('config.json', "w") as f:
    json.dump(settings, f, indent=4)
    
BotCore.tele_bool = settings['tele_bool']
BotCore.proxy_centralized = True
BotCore.max_waste_time = 900
BotCore.release = True
BotCore.mode = 'multi'
BotCore.counter_step = settings['counter_step']
TeleCore().start()
BillingCore().start()
ban_rules = BanRules()

sectors_done = 0


class ObserverBotSample(BotCore):
    driver_source = 'hrenium'

    def __init__(self, ChrTab, event_name, URL, bot_name,
                     sectors_q, **from_needed_events):
        super().__init__(ChrTab)
        self.event_name = event_name
        self.URL = URL
        self.bot_name = bot_name
        self.sectors_q = sectors_q
        self._unpack(from_needed_events)
        self.from_needed_events = from_needed_events
        self.observe_counter = 0
        self.new_settings = None
        self.settings_lock = threading.Lock()
        
    def _unpack(self, items):
        self.buy_mode = items['buy_mode']
        self.del_alones = items['del_alones']
        self.delay = items['delay']
        self.black_list = items['black_list']
        self.white_list = items['white_list']
        self.version = items['version']
        self.notify = items['notify']
        self.notify_all = items['notify_all']
        items['url'] = self.URL
        items['event_name'] = self.event_name
        
    def manage_settings(self):
        self.settings_lock.acquire()
        try:
            if self.new_settings:
                self.from_needed_events = self.new_settings
                self._unpack(self.from_needed_events)
                self.bprint('--New settings accepted--')
                self.new_settings = None
        except:
            print(yellow('Error accepting settings on bot'))
        finally:
            self.settings_lock.release()
        
    def before_body(self):
        self.from_observer = {
            'session': requests.Session()
        }
        
    def get_sectors(self):
        countable = False
        
        # if countable, every sector dict should contain 'count' key
        a_sectors = [{'name': 'A 101', 'count': 29, 'limit': 2, 'sector_id': '122377'},]
        return a_sectors, countable
        
    def filter_(self, sectors):
        def needed_black(sector):
            csector = capitalize(sector)
            for word in self.black_list:
                if capitalize(word) in csector:
                    return False
            else:
                return True
        def needed_white(sector):
            csector = capitalize(sector)
            for word in self.white_list:
                if capitalize(word) in csector:
                    return True
            else:
                return False
        sector_names = {sector['name']: sector for sector in sectors}
        not_black_sectors = [sector for sector in sector_names if
                                 needed_black(sector)]
        if not self.white_list or 'cost' in self.white_list or 'price' in self.white_list:
            not_black_data = get_by_keys(not_black_sectors,
                                         sector_names)
            return not_black_data
        in_white_sectors = [sector for sector in sector_names if
                                 needed_white(sector)]
        _, intersection, only_white = differences(not_black_sectors,
                                                  in_white_sectors)
        intersection_data = get_by_keys(intersection + only_white,
                                        sector_names)
        return intersection_data
        
    def lock(self):
        start_time = time.time()
        if (not self.notify) and (not self.buy_mode):
            while (time.time() - start_time) < 120:
                time.sleep(1)
        
    def body(self):
        self.lock()
        sectors_data, is_countable = self.get_sectors()
        fix_sectors_names(sectors_data)
        if is_countable:
            if self.white_list and not self.notify_all and 'cost' not in self.white_list:
                if 'price' not in self.white_list:
                    a_sectors = {sector['name']: sector['count'] for sector in sectors_data 
                        if any_from(self.white_list, sector['name'])}
                else:
                    raise RuntimeError('Strange situation with ``price``, need fix')
            else:
                a_sectors = {sector['name']: sector['count'] for sector in sectors_data}
        else:
            if self.white_list and not self.notify_all and 'cost' not in self.white_list:
                if 'price' not in self.white_list:
                    a_sectors = [sector['name'] for sector in sectors_data
                        if any_from(self.white_list, sector['name'])]
                else:
                    raise RuntimeError('Strange situation with ``price``, need fix')
            else:
                a_sectors = [sector['name'] for sector in sectors_data]
        if self.notify:
            self.change_ticket_state(self.event_name,
                                     a_sectors,
                                     self.URL,
                                     separator='\n',
                                     print_minus=False)
        self.from_needed_events['tele_ids'] = self.tele_ids
        sector_datas = self.filter_(sectors_data)
        if self.buy_mode:
            for sector_data in sector_datas:
                to_sector_grabber = [
                    self.from_needed_events,
                    self.from_observer,
                    sector_data
                ]
                self.sectors_q.put(to_sector_grabber)
        #while self.sector_class.working or self.order_class.working:
        #    print('--hold--')
        #    time.sleep(1)
        self.manage_settings()
        
class SectorGrabberSample(BotCore):
    driver_source = None
    ChrTab = get_chrtab()
    order_tab = ChrTab
    working = 0
    
    def __init__(self, sectors_q, tickets_q):
        super().__init__(0)
        self.sectors_q = sectors_q
        self.tickets_q = tickets_q
        
    def get_from_queue(self):
        quest = self.sectors_q.get()
        SectorGrabberSample.working += 1
        
        self.from_needed_events, \
        self.from_observer, self.sector_data = quest
        self.from_needed_limited = self.from_needed_events.copy()
        del self.from_needed_limited['black_list']
        del self.from_needed_limited['white_list']
        
    def get_tickets(self):
        a_tickets = [
            {'row': 7, 'seat': 5, 'price': 228},
            {'row': 7, 'seat': 6, 'price': 228},
            {'row': 2, 'seat': 1, 'price': 228},
            {'row': 2, 'seat': 3, 'price': 228}
        ]
        return a_tickets
        
    def before_body(self):
        pass
        
    def before_get_q(self):
        return self.before_body()
        
    def body(self):
        tickets = self.get_tickets()
        preparse(tickets)
        if not tickets:
            return True
        tickets = self.filter_(tickets)
        self.check_for_ban(tickets)
        if tickets:
            print(')', end='')
            #print("Откупаю " + self.sector_data['name'])
            #print(f'Отфильтрованных билетов в {self.sector_data["name"]} {len(tickets)}')
        else:
            return True
        self.send_tickets(tickets)
        
    def limit_rows(self, tickets, limits, white_list):
        limited_tickets = []
        if 'price' in white_list:
            white_list['cost'] = white_list['price']
        if 'cost' in white_list:
            price_range = white_list['cost']
            for ticket in tickets:
                if 'price' in ticket:
                    price = ticket['price']
                else:
                    price = ticket['cost']
                if price_range[0] <= price <= price_range[1]:
                    limited_tickets.append(ticket)
        if not limits:
            return limited_tickets
        if limits == '*':
            return tickets
        int_limits = {int(key): value for key, value in limits.items()}
        for ticket in tickets:
            if 'row' not in ticket:
                limited_tickets.append(ticket)
                continue
            row = ticket['row']
            row = int(row)
            if row not in int_limits:
                continue
            min_seat, max_seat = int_limits[row]
            if ticket['seat'] in range(min_seat, max_seat + 1):
                limited_tickets.append(ticket)
        return limited_tickets
        
    def filter_(self, tickets):
        def sort_by_rowseat(ticket):
            return ticket['row'] * 100 + ticket['seat']
        if tickets:
            if 'row' in tickets[0]:
                tickets.sort(key=sort_by_rowseat)
        if self.from_needed_events['del_alones']:
            tickets = del_alones(tickets)
        white_list = self.from_needed_events['white_list'] 
        if white_list:
            limits = None
            # Ситуация когда сектор найден
            for sector in white_list:
                if capitalize(sector) in capitalize(self.sector_data['name']):
                    limits = white_list[sector]
                    break
            tickets = self.limit_rows(tickets, limits, white_list)
        return tickets
        
    def check_for_ban(self, tickets):
        sector_name = self.sector_data['name']
        event_name = self.from_needed_events['event_name']
        a_tickets = []
        for ticket in tickets:
            if ban_rules.main_check(ticket, sector_name, event_name):
                a_tickets.append(ticket)
        tickets.clear()
        tickets.extend(a_tickets)
                                        
    def send_tickets(self, tickets):
        global sectors_done
        count = 0
        total_count = 0
        tickets_pack = []
        while tickets:
            if tickets:
                tickets_pack.append(tickets.pop())
                total_count += 1
                count += 1
            if (count == self.sector_data['limit']) or not tickets:
                SectorGrabberSample.order_tab += 1
                self.sector_data['tab'] = SectorGrabberSample.order_tab
                to_order_bot = [
                    self.from_needed_limited,
                    self.from_observer,
                    self.sector_data,
                    tickets_pack
                ]
                for _ in range(settings['order_multiplier']):
                    self.tickets_q.put(to_order_bot)
                tickets_pack = []
                count = 0
        if total_count:
            sectors_done += 1
        if sectors_done % (5 * settings['sector_threads']) == 0:
            if (self.sectors_q.qsize() / settings['sector_threads']) > 20:
                script_name = sys.argv[0]
                if ':\\' in script_name:
                    script_name = script_name.split('\\')[-1]
                mes = f'{script_name} - перегружена очередь секторов!'
                self.tprint_me(mes)
            #print(f'Отправлено {total_count} билетов')
            
    def run(self):
        while True:
            self.get_from_queue()
            
            self.before_body()
            SectorGrabberSample.ChrTab += 1
            self.ChrTab = SectorGrabberSample.ChrTab
            multi_try(self.body, fpass, 'Main', 2, self.release)
            SectorGrabberSample.working -= 1


class OrderBotSample(BotCore):
    working = 0
    ready = 0
    
    def __init__(self, tickets_q, accounts=None):
        super().__init__(0)
        self.tickets_q = tickets_q
        if accounts:
            self.accounts = accounts
        self.cart_q = Queue()
        self.cart_threads = settings['cart_threads']
    
    def get_from_queue(self):
        self.from_needed_events, self.from_observer, \
        self.sector_data, self.tickets_pack = self.tickets_q.get()
        
        self.ChrTab = self.sector_data['tab']
        self.tele_ids = self.from_needed_events['tele_ids']
               
    def send_descrs(self, url=None):
        ticket_descrs = '\n'.join(self.ticket_descrs)
        event_name = self.from_needed_events['event_name']
        all_descr = (f"{event_name}\n{self.sector_data['name']}"
                     f"\n{ticket_descrs}")
                     
        if 'url' in self.from_needed_events:
            event_url = str(self.from_needed_events['url'])
            all_descr += ("\nСхема: " + event_url)
        if hasattr(self, 'account'):
            all_descr += ("\nАккаунт "
                         f"{self.account.login} {self.account.password}")
        if url and (url != True):
            all_descr += "\nОплатить: " + url
        self.tprint_billing(all_descr, only_log=True)
        #try:
        #    self.tprint(all_descr, only_log=True)
        #except:
        #    all_descr = 'ОПЛАТЫ (запасной вывод) ' + all_descr
        #    self.tprint(all_descr, only_log=True)
            
    def adder(self):
        ticket = self.cart_q.get()
        if ticket:
            ticket_descr = self.add_to_cart(ticket)
            if ticket_descr:
                self.ticket_descrs.append('--' + ticket_descr)
        self.finished_adders += 1
               
    def create_order(self):
        """
        should return payment link
        If link cannot be shown, return True if order
        placed, else False if order creation went wrong instead
        Example:
        return '"result":true' in r.text
        """
        return True
               
    def checkout(self):
        if not self.ticket_descrs:
            print('Пустой чекаут')
            if hasattr(self, 'account'):
                self.account.deauthorize()
                self.accounts.put(self.account)
            return False
        mes = 'Корзина: ' + str(len(self.ticket_descrs))
        print(green(mes))
        order_result = self.create_order()
        if order_result:
            print(green("Чекаут: Успешно вывело на оплату!"), end='')
            ban_rules.add_to_ban_list(self.added_to_cart,
                                      self.sector_data['name'],
                                      self.from_needed_events['event_name'])
            self.send_descrs(order_result)
        else:
            print(red("Чекаут: Не выведено на оплату!\n"), end='')
            if hasattr(self, 'account'):
                self.account.deauthorize()
                self.accounts.put(self.account)
            
    def add_to_cart(self, ticket):
        """
        Example:
        if 'row' in ticket:
            ticket_descr = (f'Ряд {ticket["row"]}, '
                            f'Место {ticket["seat"]}, '
                            f'Цена {ticket["price"]} руб')
        else:
            ticket_descr = ('Неизвестное место, '
                            f'Цена {ticket["price"]} руб')
        if '"result":true' in r.text:
            return ticket_descr
        else:
            print("Спизжено:" + r.text[:40] + '\n', end='')
            return None
        """
        return 'Some ticket discription'
            
    def body(self):
        self.put_tickets = 0
        self.ticket_descrs = []
        self.added_to_cart = []
        if self.cart_threads:
            for ticket in self.tickets_pack:
                self.cart_q.put(ticket)
                self.put_tickets += 1
            while self.finished_adders != self.put_tickets:
                time.sleep(0.1)
            self.checkout()
        else:
            for ticket in self.tickets_pack:
                ticket_descr = self.add_to_cart(ticket)
                if ticket_descr:
                    self.added_to_cart.append(ticket)
                    self.ticket_descrs.append('--' + ticket_descr)
            self.checkout()
               
    def before_order(self):
        return self.after_get_q()
        
    def before_get_q(self):
        pass
        
    def after_get_q(self):
        pass
        
    def on_except(self):
        if hasattr(self, 'accounts') and hasattr(self, 'account'):
            print(yellow('Account Returned\n'), end='')
            self.account.deauthorize()
            self.accounts.put(self.account)
        print('Чекаут: ЭКСЕПШЕН!!!\n', end='')
               
    def run(self):
        while True:
            self.finished_adders = 0
            for _ in range(self.cart_threads):
                threading.Thread(target=self.adder).start()
            
            OrderBotSample.ready += 1
            multi_try(self.before_get_q, fpass, 'Sub', 1, self.release)
            self.get_from_queue()
            multi_try(self.before_order, fpass, 'Sub', 1, self.release)
            OrderBotSample.ready -= 1
            
            OrderBotSample.working += 1
            multi_try(self.body, self.on_except, 'Main', 1, self.release)
            OrderBotSample.working -= 1
            
            if not self.cart_threads:
                continue
            for _ in range(self.cart_threads - self.put_tickets):
                self.cart_q.put(None)


def reload_settings(needed_events):
    for event_name, _, url, settings in needed_events:
        bot = url_on_bots[url]
        if bot.version != settings['version']:
            bot.settings_lock.acquire()
            try:
                bot.new_settings = settings
            finally:
                bot.settings_lock.release()
                vers = settings['version']
                mes = (f'Releasing {bot.short_name} '
                       f'settings from #{bot.version} to #{vers}')
                print(yellow(mes))
                
                
def restart_threads(needed_events, observer_class, sectors_q, bots, accounts=None):
    global url_on_bots
    old_urls = url_on_bots.keys()
    new_events = {event[2]: event for event in needed_events}
    to_stop, _, to_start = differences(old_urls, new_events.keys())
    
    for url in to_stop:
        bot = url_on_bots[url]
        bot.stop()
        print(yellow(f'Bot {bot} stopped!'))
        if hasattr(bot, 'account'):
            accounts.put(bot.account)
        del url_on_bots[url]
        bots.remove(bot)
        
    new_needed_events = [new_events[url] for url in to_start]
    new_bots = start_bots(new_needed_events, observer_class, False,
                          first=False, args=[sectors_q], is_buying_bot=True)
    bots.extend(new_bots)
    new_url_on_bots = {bot.URL: bot for bot in new_bots}
    url_on_bots.update(new_url_on_bots)
                
                
def reimport_settings_thread(observer_class, sectors_q, bots, accounts=None):
    def reimport():
        start_time = time.time()
        #delete_module('needed')
        #import needed
        #restart_threads(needed.needed_events, observer_class, sectors_q, accounts)
        #reload_settings(needed.needed_events)
        with open('needed.json', encoding='utf-8') as needed:
            needed_events = json.load(needed)
        restart_threads(needed_events, observer_class, sectors_q, bots, accounts)
        reload_settings(needed_events)
    to_except = lambda _: print('Error reimporting settings')
    while True:
        time.sleep(settings['reimport_delay'])
        multi_try(reimport, to_except, 'Sub', 1, True)
        
        
def args_by_os():
    if len(sys.argv) == 1:
        return None
    else:
        return sys.argv[1:]
        
        
def args_by_os_default():
    if len(sys.argv) == 1:
        start_buying_bot = True
        start_event_bot = True
    else:
        args = [bool(int(arg)) for arg in sys.argv[1:]]
        start_buying_bot, start_event_bot = args
    return start_buying_bot, start_event_bot
        
        
def monitor(SectorGrabber, OrderBot, manager_socket, monitor_q=None):
    print('SectorGrabber.working', SectorGrabberSample.working)
    print('OrderBot.working', OrderBotSample.working)
    print('OrderBot.ready', OrderBotSample.ready)
    if monitor_q:
        print('qsize', monitor_q.qsize())
    print(manager_socket)
    
    
def start_buying_bots(observer_class, sector_class, order_class,
                      sectors_q, tickets_q, accounts_q=None):
    start_buying_bot, _ = args_by_os_default()
    if not start_buying_bot:
        return 'Запущен с _e параметрами. Сокет откупщика не запущен'
    observer_class.sector_class = sector_class
    observer_class.order_class = order_class
    
    bots = []
    socket_info = bot_socket.run_socket(bots, accounts_q, is_buying_bot=True)
    global url_on_bots
    with open('needed.json', encoding='utf-8') as needed:
        needed_events = json.load(needed)
    new_bots = start_bots(needed_events, observer_class, False,
                          args=[sectors_q], is_buying_bot=True)
    bots.extend(new_bots)
    url_on_bots = {bot.URL: bot for bot in bots}
        
    threading.Thread(target=reimport_settings_thread,
                     args=(observer_class, sectors_q,
                           bots, accounts_q)).start()
    if settings['order_multiplier'] != 1:
        mes = f'BE CAREFUL! ORDER MULTIPLIER IS EQUAL TO {settings["order_multiplier"]}'
        print(green(mes))
    
    for _ in range(settings['sector_threads']):
        sector_class(sectors_q, tickets_q).start()
    for _ in range(settings['order_threads']):
        order_args = [tickets_q]
        order_kwargs = {}
        if accounts_q:
            order_kwargs['accounts'] = accounts_q
        order_class(*order_args, **order_kwargs).start()
        
    return socket_info
        

def start_event_parser(ev_name, url, parser_class=None, auto_chrtab=False):
    def event_parse():
        with open('needed.json', encoding='utf-8') as needed:
            needed_events = json.load(needed)
        if needed_events:
            ev_tele_profiles = needed_events[0][1]
        else:
            ev_tele_profiles = "we"
        
        needed_events_evbot = [
            (
                ev_name,
                ev_tele_profiles,
                url,
                {
                    'url_on_bots': url_on_bots
                }
            )
        ]
        start_bots(needed_events_evbot, parser_class, auto_chrtab, is_buying_bot=False)
    _, start_event_bot = args_by_os_default()
    if not start_event_bot:
        return False
    if not os.path.exists('event_bot.py'):
        return False
    multi_try(event_parse, fpass, 'EventParser', 1, True)
    
    
def start_accounts_queue(QueueClass, txt='authorize_accounts.txt', **kwargs):
    if args_by_os_default()[0]:
        accounts = QueueClass(txt, **kwargs)
        accounts.start()
        return accounts
    
            
def load_names():
    name = lambda n: f'register\\{n}Name_M_rus.txt'
    with open(name(''), 'r', encoding='utf-8') as regfile:
        regtxt = regfile.read()
        names = regtxt.split('\n')
    with open(name('Second_'), 'r', encoding='utf-8') as regfile:
        regtxt = regfile.read()
        sec_names = regtxt.split('\n')
    with open(name('Middle_'), 'r', encoding='utf-8') as regfile:
        regtxt = regfile.read()
        mid_names = regtxt.split('\n')
    return names, sec_names, mid_names
    
    
def get_identity():
    return random.choice(first_ns), \
           random.choice(second_ns), \
           random.choice(middle_ns)
    

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
        
        
def preparse(tickets):
    for ticket in tickets:
        try:
            ticket['row'] = int(ticket['row'])
        except:
            pass
        try:
            ticket['seat'] = int(ticket['seat'])
        except:
            pass
        if 'price' in ticket:
            ticket['price'] = int(ticket['price'])
            
def del_alones(tickets):
    rownumbers = [int(ticket['row']) for ticket in tickets]
    seatnumbers = [int(ticket['seat']) for ticket in tickets]
    max_row = max(rownumbers)
    seats = [[] for i in range(max_row + 1)]
    for row, seat, ticket in zip(rownumbers, seatnumbers, tickets):
        seats[row].append([seat, ticket])
    sort_func = lambda item: item[0]
    for i in range(len(seats)):
        seats[i] = sorted(seats[i], key=sort_func)
    parsed = []
    for (i, row) in enumerate(seats):
        for col, ticket in row:
            cols = [item[0] for item in row]
            if (col - 1 in cols) or (col + 1 in cols):
                parsed.append(ticket)
    return parsed
            
def capitalize(str_):
    return str_.replace(' ', '').lower()
    
    
def get_by_keys(names, dict_):
    return [dict_[name] for name in names]


def month(source):
    source = int(source)
    months = {1: 'Янв', 2: 'Фев', 3: 'Мар', 4: 'Апр',
              5: 'Май', 6: 'Июн', 7: 'Июл', 8: 'Авг',
              9: 'Сен', 10: 'Окт', 11: 'Ноя', 12: 'Дек'}
    return months[source]


def fix_sectors_names(sectors_data):
    for sector in sectors_data:
        sector['name'] = main_utils.unicode_fix(sector['name'])


url_on_bots = {}
first_ns, second_ns, middle_ns = load_names()

"""
if __name__ == '__main__':
    # Defining global variables
    sectors_q = Queue()
    tickets_q = Queue()
    accounts = athorization.BolshoiQueue('authorize_accounts.txt', 3600)
    accounts.start()
    
    # Starting buying threads
    start_buying_bots(ObserverBot, SectorGrabber,
                      OrderBot, sectors_q, tickets_q)
    while True:
        input()
        monitor(SectorGrabber, OrderBot)
"""