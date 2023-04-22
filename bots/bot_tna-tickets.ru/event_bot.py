from cores_src.event_bot_sample import *
from authorization import TNAQueue


class EventParser(EventParserSample):
    driver_source = None
    counter_step = 5
    delay = 120

    def __init__(self, ChrTab, event_name, URL, bot_name,
                 api_token, **init_kwargs):
        super().__init__(ChrTab, event_name, URL, bot_name, **init_kwargs)
        self.api_token = api_token
        self.url_on_events = {}
        self.session = None
        # self.account = None

    def before_body(self):
        self.session = main_utils.ProxySession(self)
        # self.account = accounts.get()

    def format_date(self, date):
        month_list = [
            "", "Янв", "Фев", "Мар", "Апр",
            "Май", "Июн", "Июл", "Авг",
            "Сен", "Окт", "Ноя", "Дек"
        ]

        d_m_y, time = date.split()
        d, m, y = d_m_y.split('.')
        month = month_list[int(m)]
        time = time[:-3]
        date = f'{d} {month} {y} {time}'
        return date

    def get_a_events(self):
        assert self.api_token is not None, 'token needs to be set'
        url = f'https://api.tna-tickets.ru/api/v1/game?access-token={self.api_token}&sport=1'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,ima'
                      'ge/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }
        r = self.session.get(url, headers=headers)

        if '"status":200' not in r.text:
            raise RuntimeError('--Не получен запрос--', r.text[:100])

        events = r.json()['result']
        a_events = []
        for event in events:
            title = event['name']
            date = self.format_date(event['active_to'])
            url = self.URL + str(event['properties']['booking_id'])
            event = f'{title}. {date}'
            a_events.append(event)
            self.url_on_events[event] = url

        return a_events

    def get_event_page(self, event_name):
        return None

    def get_event_url(self, event_name, page):
        return self.url_on_events[event_name]

    def get_full_ev_name(self, event_name, page):
        # event: str
        # city: str
        # day: int
        # month: str
        # time_: str
        city = 'Мск'
        event_items = event_name.split('. ')
        full_date = event_items.pop()
        event_name = '. '.join(event_items)
        d, m, y, time_ = full_date.split(' ')
        return event_name, city, int(d), m, time_


if __name__ == '__main__':
    api_token = '5f4dbf2e5629d8cc19e7d51874266678'
    # accounts = TNAQueue('event_bot_authorize_accounts.txt', api_token, reauthorize=True)
    # accounts.start()
    # time.sleep(20)

    with open('config.json') as f:
        settings = json.load(f)

    BotCore.tele_bool = settings['tele_bool']
    BotCore.proxy_centralized = True
    BotCore.mode = 'multi'
    BotCore.counter_step = 20
    BotCore.max_waste_time = 10000
    TeleCore().start()

    start_event_parser('Ак-Барс. Мск. ',
                       'https://www.ak-bars.ru/tickets/',
                       EventParser)
