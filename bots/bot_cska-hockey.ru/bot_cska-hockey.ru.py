from cores_src.bot_sample_server import *
from event_bot import EventParser
import authorization

BotCore.tele_bool = settings['tele_bool']
BotCore.release = True
BotCore.proxy_centralized = False


class ObserverBot(ObserverBotSample):
    
    def __init__(self, *init_args, **from_needed_events):
        super().__init__(*init_args, **from_needed_events)
        self.from_observer = None
        self.event_id = None
        self.csrf_frontend = None
        self.x_csrf_token = None
        self.session = None

    def before_body(self):
        self.session = requests.Session()
        self.x_csrf_token, self.csrf_frontend = self.get_tokens()
        self.event_id = self.URL.split('=')[1].split('/')[0]

        self.from_observer = {
            'event_id': self.event_id,
            'x_csrf_token': self.x_csrf_token,
            'csrf_frontend': self.csrf_frontend,
            'session': self.session,
            'proxies': self.requests_proxies()
        }
    
    def get_tokens(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avi'
                      'f,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }
        r = self.session.get(self.from_needed_events['url'], headers=headers,
                             proxies=self.requests_proxies(), verify=False)
        if 'queue' in r.url:
            queue_id = double_split(r.text, 'serverRendered:', '</script')
            queue_id = double_split(queue_id, '"', '"')
            r = self.solve_queue(r, queue_id, headers)
            if not r:
                raise RuntimeError('Бот не смог пройти очередь')

        x_csrf_token = double_split(r.text, 'name="csrf-token" content="', '"')
        _csrf_frontend = double_split(r.text, 'name="_csrf-frontend" value="', '"')

        return x_csrf_token, _csrf_frontend
        
    def renew_session(self, r):
        self.slide_tab()
        self.session = requests.Session()
        self.x_csrf_token, self._csrf_frontend = self.get_tokens()
        self.bprint(self.get_proxy()[1])
        self.bprint(self.x_csrf_token)
        raise RuntimeError(r.text[:70])
    
    def solve_queue(self, r, queue_id, headers):
        queue_site = double_split(r.text, '<span class="d-block">', '</span>')
        self.tprint(f'Бот попал в очередь, номер в очереди - {queue_site}')
        print(f'Бот попал в очередь, номер в очереди - {queue_site}')
        tries = 0
        while 'queue' in r.url:
            if tries == 25:
                print('Бот не смог пройти очередь')
                return False
            time.sleep(5)
            url = f'https://tickets.cska-hockey.ru/?queue={queue_id}'
            r = self.session.get(url, headers=headers, proxies=self.requests_proxies())
            tries += 1
        r = self.session.get(self.URL, headers=headers, proxies=self.requests_proxies())
        return r
        
    def get_request(self):
        headers = {
            'authority': 'tickets.cska-hockey.ru',
            'method': 'GET',
            'path': f'/event/?id={self.event_id}',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,ima'
                      'ge/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }
        r = self.session.get(self.URL, headers=headers,
                             proxies=self.requests_proxies(), verify=False)
        if 'queue' in r.url:
            queue_id = double_split(r.text, 'serverRendered:', '</script')
            queue_id = double_split(queue_id, '"', '"')
            r = self.solve_queue(r, queue_id, headers)
            if not r:
                raise RuntimeError('Бот не смог пройти очередь')
        return r
        
    def get_sectors(self):
        countable = True
        
        r = self.get_request()
        if 'sub-title' not in r.text:
            raise RuntimeError('--Page load error--')
        has_free = lambda elem: 'free="' in elem
        g_elems = [elem for elem in lrsplit(r.text, '<g id="', '>') if has_free(elem)]
        g_count = len(g_elems)
        self.bprint(f'Count of g-elems: {g_count}')
        free = lambda elem: double_split(elem, 'free="', '"')
        price = lambda elem: double_split(elem, 'price="', '"')
        view_id = lambda elem: double_split(elem, 'view_id="', '"')
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
        sector_nam = lambda elem: double_split(elem, 'sector_name="', '"')
        sector_name = lambda elem: sectors_dict[sector_nam(elem)] \
                          if sector_nam(elem) in sectors_dict else sector_nam(elem)
        limit = 4
        a_sectors = [{
            'name': sector_name(g),
            'limit': limit,
            'count': int(free(g)),
            'view_id': view_id(g)
        } for g in g_elems]
        return a_sectors, countable
        
        
class SectorGrabber(SectorGrabberSample):
    def __init__(self, *init_args):
        super().__init__(*init_args)
        
    def tickets_request(self, view_id):
        url = 'https://tickets.cska-hockey.ru/event/get-actual-places'
        headers = {
            'authority': 'tickets.cska-hockey.ru',
            'method': 'POST',
            'path': '/event/get-actual-places',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '149',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://tickets.cska-hockey.ru',
            'pragma': 'no-cache',
            'referer': self.from_needed_limited['url'],
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-csrf-token': self.from_observer['x_csrf_token'],
            'x-requested-with': 'XMLHttpRequest'
        }
        data = {
            'event_id': self.from_observer['event_id'],
            'view_id': view_id,
            'clear_cache': False,
            '_csrf-frontend': self.from_observer['csrf_frontend']
        }
        r = self.session.post(url, data=data, headers=headers,
                              proxies=self.observer_proxy, verify=False)
        return r.json()['places']['values']
        
    def get_tickets(self):
        self.session = self.from_observer['session']
        self.observer_proxy = self.from_observer['proxies']
        view_id = self.sector_data['view_id']
        tickets = self.tickets_request(view_id)
        for ticket in tickets:
            row = double_split(ticket['id'], 'r', 'p')
            seat = ticket['id'].split('p')[1]
            ticket['row'] = int(row)
            ticket['seat'] = int(seat)
        return tickets
        
        
class OrderBot(OrderBotSample):
    def __init__(self, *init_args, **init_kwargs):
        super().__init__(*init_args, **init_kwargs)
        self.payment_id = None

    def get_tokens(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif'
                      ',image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'connection': 'keep-alive',
            'host': 'tickets.cska-hockey.ru',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }

        r = self.account.get(self.from_needed_events['url'],
                             headers=headers, verify=False)

        x_csrf_token = double_split(r.text, 'name="csrf-token" content="', '"')
        csrf_frontend = double_split(r.text, 'name="_csrf-frontend" value="', '"')

        return x_csrf_token, csrf_frontend
    
    def before_order(self):
        self.account = accounts.get()
        self.x_csrf_token, self.csrf_frontend = self.get_tokens()
        headers = {
            'authority': 'tickets.cska-hockey.ru',
            'method': 'GET',
            'path': '/orders/cart',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,ima'
                      'ge/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': self.from_needed_events['url'],
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }
        cart_url = 'https://tickets.cska-hockey.ru/orders/cart'
        r = self.account.get(cart_url, headers=headers, verify=False)

        cart_tickets = lrsplit(r.text, 'tickets__item ', 'span')
        if not cart_tickets:
            return True
        headers = {
            'authority': 'tickets.cska-hockey.ru',
            'method': 'DELETE',
            'path': '/event/cart/remove',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '132',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://tickets.cska-hockey.ru',
            'pragma': 'no-cache',
            'referer': 'https://tickets.cska-hockey.ru/orders/cart',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-csrf-token': self.x_csrf_token,
            'x-requested-with': 'XMLHttpRequest'
        }
        remove_url = 'https://tickets.cska-hockey.ru/event/cart/remove'
        for ticket in cart_tickets:
            self.bprint(f'deleting on {self.account}')
            remove_data = [
                ('sid', double_split(ticket, 'data-place="', '"')),
                ('event_id', double_split(ticket, 'data-event="', '"')),
                ('_csrf-frontend', self.csrf_frontend)
            ]
            r = self.account.delete(remove_url, data=remove_data,
                                    headers=headers, verify=False)
            
    def add_to_cart(self, ticket):
        headers = {
            'authority': 'tickets.cska-hockey.ru',
            'method': 'POST',
            'path': '/event/cart/add',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '145',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://tickets.cska-hockey.ru',
            'pragma': 'no-cache',
            'referer': self.from_needed_events['url'],
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-csrf-token': self.x_csrf_token,
            'x-requested-with': 'XMLHttpRequest'
        }
        form_data = [
            ('sid', ticket['id']),
            ('event_id', self.from_observer['event_id']),
            ('view_id', self.sector_data['view_id']),
            ('_csrf-frontend', self.csrf_frontend)
        ]
        url_add = 'https://tickets.cska-hockey.ru/event/cart/add'
        r = self.account.post(url_add, data=form_data,
                              headers=headers, verify=False)
        jsoned = r.json()
        
        if 'carts' in jsoned:
            if not jsoned['carts']:
                self.bad_add(r.text)
                return None
            row = jsoned['carts'][0]['row']
            seat = jsoned['carts'][0]['col']
            cost = jsoned['carts'][0]['price']
            self.payment_id = jsoned['carts'][0]['payment_id']

            ticket_descr = (f'Ряд {row}, '
                            f'Место {seat}, '
                            f'Стоимость {cost} руб')
            return ticket_descr
        else:
            self.bad_add(r.text)
            return None

    def bad_add(self, rtext):
        jsoned = json.loads(rtext)
        if 'redraw' in jsoned:
            print(red("Спизжено"))
        elif 'limit' in jsoned:
            print(red("Лимит"))
        elif 'подтвердить номер' in rtext:
            accounts.ban(self.account)
            print(red('Неподтвержденный номер телефона, бан'))
        else:
            print(red('Add to cart error ' + rtext[:60]))

    def create_order(self):
        # Input data:
        #   self.from_needed_events - input data for event from needed.py
        #   self.from_observer - specific data for whole event
        #   self.sector_data - entire data on sector
        #   self.tickets_pack - all tickets are here
        #   self.ticket_descrs - all succeeded ticket descriptions
        headers = {
            'authority': 'tickets.cska-hockey.ru',
            'method': 'GET',
            'path': f'/pay/pay?id={self.payment_id}',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,ima'
                      'ge/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://tickets.cska-hockey.ru/orders/cart',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }
        confirm_url = f'https://tickets.cska-hockey.ru/pay/pay?id={self.payment_id}'
        r = self.account.get(confirm_url, headers=headers, allow_redirects=False,
                             verify=False)
        if 'Location' not in r.headers:
            return None
        if 'vbrr' not in r.headers['Location']:
            return None
        return r.headers['Location']


if __name__ == '__main__':
    scripted = args_by_os()
    
    # Starting account pool
    accounts = start_accounts_queue(authorization.CSKAHQueue, reauthorize=True)
    
    # Defining global variables
    tickets_q = Queue()
    sectors_q = Queue()
    
    # Starting buying threads
    manager_socket = start_buying_bots(ObserverBot, SectorGrabber, OrderBot, sectors_q,
                                       tickets_q, accounts_q=accounts)

    start_event_parser('ЦСКА Хоккей. Мск. ', 'https://tickets.cska-hockey.ru/', EventParser)
    while True:
        input()
        monitor(SectorGrabber, OrderBot, manager_socket, monitor_q=accounts)
