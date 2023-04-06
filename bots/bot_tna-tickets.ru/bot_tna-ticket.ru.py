from cores_src.bot_sample_server import *
import authorization

BotCore.tele_bool = settings['tele_bool']
BotCore.release = True
BotCore.proxy_centralized = False


class ObserverBot(ObserverBotSample):
    driver_source = 'hrenium'

    def __init__(self, *init_args, **from_needed_events):
        super().__init__(*init_args, **from_needed_events)
        self.account = None
        self.from_observer = None
        self.session = None

    def before_body(self):
        self.account = self.accounts.get()
        self.prepare_session()
        self.from_observer = {
            'session': self.session,
            'proxies': self.requests_proxies()
        }

    def get_request(self):
        headers = {
            'authority': 'tickets.cska-hockey.ru',
            'method': 'GET',
            'path': f'/event/?id={self.event_id}',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
        r = self.session.get(self.URL, headers=headers, proxies=self.requests_proxies())
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
            'referer': self.from_needed_events['url'],
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
        r = self.session.post(url, data=data, headers=headers, proxies=self.observer_proxy)
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
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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

        r = self.account.get(self.from_needed_events['url'], headers=headers)

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
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
        r = self.account.get(cart_url, headers=headers)

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
            r = self.account.delete(remove_url, data=remove_data, headers=headers)

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
        r = self.account.post(url_add, data=form_data, headers=headers)
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
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
        r = self.account.get(confirm_url, headers=headers, allow_redirects=False)
        if 'Location' not in r.headers:
            return None
        if 'vbrr' not in r.headers['Location']:
            return None
        return r.headers['Location']


def get_api_token(session):
    url = 'https://www.ak-bars.ru/'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
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
        'user-agent': BotCore.user_agent
    }
    r = session.get(url, headers=headers)
    if 'data-hid="gtm-noscript" data-pbody="true"' not in r.text:
        raise RuntimeError('The page was not loaded')
    script_dirs = lrsplit(r.text, 'link rel="preload" href="', '"')

    script_url = script_dirs[-2]
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'connection': 'keep-alive',
        'host': 'www.ak-bars.ru',
        'pragma': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': BotCore.user_agent
    }
    r = session.get(script_url, headers=headers)
    if 'TNA_API_KEY: "' not in r.text:
        raise RuntimeError('No API key found in JS. Auth method might be changed')
    return double_split(r.text, 'TNA_API_KEY: "', '"')


if __name__ == '__main__':
    scripted = args_by_os()

    # Starting account pool
    api_token = get_api_token(requests.Session())
    accounts = start_accounts_queue(authorization.TNAQueue, api_token)

    # Defining global variables
    tickets_q = Queue()
    sectors_q = Queue()

    # Starting buying threads
    manager_socket = start_buying_bots(ObserverBot, SectorGrabber,
                                       OrderBot, sectors_q, tickets_q,
                                       accounts_q=accounts)
    start_event_parser('ЦСКА Хоккей. Мск. ', 'https://tickets.cska-hockey.ru/')
    while True:
        input()
        monitor(SectorGrabber, OrderBot, manager_socket)