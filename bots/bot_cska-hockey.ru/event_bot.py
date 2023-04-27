from cores_src.event_bot_sample import *


class EventParser(EventParserSample):
    driver_source = None
    counter_step = 1
    delay = 360

    def __init__(self, *init_args, **init_kwargs):
        super().__init__(*init_args, **init_kwargs)
        self.session = None
        self.url_on_events = {}
        
    def before_body(self):
        self.session = main_utils.ProxySession(self)
        
    def get_a_events(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'
                      ',image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }
        r = self.session.get(self.URL, headers=headers, verify=False)
        if 'matches-content' not in r.text:
            raise RuntimeError('--Не получен запрос--')
            
        # Getting available events in any format
        a_events = []
        event_areas = r.text.split('"matches-content-wrap"')
        event_areas.pop(0)
        for event_area in event_areas:
            name_area = double_split(event_area, 'matches-content-wrap-game', '</div>')
            name = double_split(name_area, '<p>', '</p>').strip()
            date_area = double_split(event_area, 'matches-content-wrap-date', '</div>')
            date = double_split(date_area, '<p>', '</p>').strip()
            time_area = double_split(event_area, 'matches-content-wrap-time', '</div>')
            time_ = double_split(time_area, '<p>', '</p>').strip()
            url_area = double_split(event_area, 'matches-content-wrap-button', '</div>')
            if 'href' not in url_area:
                continue
            url = double_split(url_area, 'href="', '"').strip()
            url = 'https://tickets.cska-hockey.ru' + url
            event = f'{name}. {date} {time_}'
            for _ in range(3):
                event = event.replace('  ', ' ')
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
        if '.20' in full_date:
            dm, time_ = full_date.split(' ')
            d, m, _ = dm.split('.')
            m = month_list[int(m)]
        else:
            d, m, _, time_ = full_date.split(' ')
        return event_name, city, int(d), m, time_


month_list = [
    "", "Янв", "Фев", "Мар", "Апр",
    "Май", "Июн", "Июл", "Авг",
    "Сен", "Окт", "Ноя", "Дек"
]

if __name__ == '__main__':
    with open('config.json') as f:
        settings = json.load(f)
    
    BotCore.tele_bool = settings['tele_bool']
    BotCore.proxy_centralized = False
    BotCore.mode = 'multi'
    BotCore.counter_step = 20
    BotCore.max_waste_time = 10000
    
    start_event_parser('ЦСКА Хоккей. Мск. ',
                       'https://tickets.cska-hockey.ru/',
                       EventParser)
    