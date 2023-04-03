import os
import sys

from .cores import *
from .vis import *
from .bot_sample_server import start_event_parser


class EventParserSample(BotCore):
    driver_source = None
    counter_step = 20
    delay = 3

    def __init__(self, ChrTab, event_name, URL, bot_name, **kwargs):
        super().__init__(ChrTab)
        self.event_name = event_name
        if isinstance(URL, str):
            self.URLs = [[None, URL]]
            self.URL = URL
        else:
            self.URLs = urls_format(URL)
            self.URL = self.URLs[0][1]
        self.bot_name = bot_name
        self.url_on_bots = kwargs['url_on_bots']
        #self.white_lists = kwargs['white_lists']
        self.url_on_events = {}
        
    def before_body(self):
        pass
            
    def prepare_to_start(self, event_name):
        page = self.get_event_page(event_name)
        url = self.get_event_url(event_name, page)
        if not url:
            raise RuntimeError('Empty URL: ' + event_name)
        
        ev, city, d, m, t = self.get_full_ev_name(event_name, page)
        m = m.capitalize()[:3]
        d = str(d)
        if len(d) == 1:
            d = '0' + d
        city = city.capitalize()
        ev = ev.replace('.', ',')
        full_ev_name = f'{ev}. {city}. {d} {m} {t}'
        
        event_params = self.filtrate(full_ev_name)
        if event_params == None:
            return True
            
        self.start_bot(full_ev_name, url, *event_params)
    
    def check_for_redirect(self, event_name, black_list):
        for event in black_list:
            if event.lower() in event_name.lower():
                return False
        return True
    
    def filtrate(self, new_event_name):
        redirect = True
        for event in self.to_needed:
            for key in event[0]:
                if key.lower() not in new_event_name.lower():
                    break
                if isinstance(event[2], list):
                    redirect = self.check_for_redirect(new_event_name, event[2])
                if not redirect:
                    break
            else:
                return event[1], event[3]
        return None
        
    def start_bot(self, event_name, url, tele_profiles, parameters):
        combined_event = [
            event_name,
            tele_profiles,
            url,
            parameters
        ]
        
        with open('needed.json', encoding='utf-8') as needed:
            needed_events = json.load(needed)
        
        for event in needed_events:
            if event_name == event[0]:
                break
            if url == event[2]:
                break
        else:
            #self.tprint(f'Направляю мероприятие на откупку: {event_name}\n{url}')
            self.send_telegram_to(f'Направляю мероприятие на откупку: {event_name}\n{url}', tele_profiles)
            needed_events.append(combined_event)
            save_needed('needed.json', needed_events)
        
    def body(self):
        for event_name, url in self.URLs:
            self.URL = url
            a_events = self.get_a_events()
                
            if len(self.URLs) > 1:
                site_name = self.event_name.split('. ')[0]
                event_name_parsed = event_name + '. ' + site_name + '. '
            else:
                event_name_parsed = self.event_name
            if self.first:
                new_events = a_events
                self.tickets_state[event_name_parsed] = a_events
            else:
                new_events = self.change_ticket_state(event_name_parsed, a_events,
                                                      url, separator='\n',
                                                      appeared='мероприятия')
            for event in new_events:
                multi_try(self.prepare_to_start, fpass, 'Sub', 1, args=(event,))
                time.sleep(0.1)
        return True
            
    def get_a_events(self):
        """
        Example:
        r = self.session.get(url, headers=headers, verify=False,
                             proxies=self.requests_proxies())
        if 'event-line' not in r.text:
            raise RuntimeError('--Не получен запрос--')
            
        # Getting available events in any format
        a_events = [
            'Свадьба Фигаро. Москва. 18 Фев 12:00',
            'Свадьба Фигаро. Москва. 18 Фев 19:00'
        ]
        return a_events
        """
        a_events = [
            'Свадьба Фигаро. Москва. 18 Фев 12:00',
            'Свадьба Фигаро. Москва. 18 Фев 19:00'
        ]
        return a_events
        
    def get_event_page(self, event_name):
        # If you don't need an additional request
        # to obtain event url or event date
        return None
        
    def get_event_url(self, event_name, page):
        return self.url_on_events[event_name]
        
    def get_full_ev_name(self, event_name, page):
        """
        event: str
        city: str
        dat: int
        month: str
        time_: str
        function todate() may be useful
        It will return today date
        Example:
        city = 'Мск'
        event, day, month, time_ = parse_this_shit(event_name)
        """
        event, city, day, month, time_ = 'Traviata', 'Moscow', 1, 'Cен', '19:00'
        return event, city, day, month, time_
        
    def run(self):
        with open('to_needed.json', encoding='utf-8') as to_needed:
            self.to_needed = json.load(to_needed)
        super().run()


def urls_format(urls):
    if isinstance(urls, dict):
        new_urls = [[dict_url[0], dict_url[1]] for dict_url in urls.items()]
        return new_urls
    else:
        return urls
        
        
def todate(inc=0):
    d = time.strftime('%d')
    m = time.strftime('%m')
    m_parsed = months[m]
    return d + ' ' + m_parsed
    
        
def save_needed(fpath, needed_events, max_indent=5):
    for _ in range(3):
        try:
            #to_save = 'needed_events = ' + json.dumps(needed_events, indent=4)
            #to_save = json_to_py(to_save, max_indent)
            to_save = json.dumps(needed_events, indent=4, ensure_ascii=False)
            indents = ' ' * max_indent * 4
            to_save = to_save.replace(',\n' + indents + '    ', ', ') \
                             .replace('\n' + indents + '    ', '') \
                             .replace('\n' + indents + ']\n', ']\n') \
                             .replace('\n' + indents + '],\n', '],\n') \
                             .replace('\n' + indents + '}\n', '}\n') \
                             .replace('\n' + indents + '},\n', '},\n')
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(to_save)
            return True
        except:
            lprint('Error saving file')
            time.sleep(0.5)
    else:
        raise RuntimeError('Error saving file in 3 times')
            
            
months = {'01': 'Янв', '02': 'Фев', '03': 'Мар', '04': 'Апр',
          '05': 'Май', '06': 'Июн', '07': 'Июл', '08': 'Авг',
          '09': 'Сен', '10': 'Окт', '11': 'Ноя', '12': 'Дек',
          '1': 'Янв', '2': 'Фев', '3': 'Мар', '4': 'Апр',
          '5': 'Май', '6': 'Июн', '7': 'Июл', '8': 'Авг',
          '9': 'Сен',
          1: 'Янв', 2: 'Фев', 3: 'Мар', 4: 'Апр',
          5: 'Май', 6: 'Июн', 7: 'Июл', 8: 'Авг',
          9: 'Сен', 10: 'Окт', 11: 'Ноя', 12: 'Дек'}

"""
if __name__ == '__main__':
    from config import *
    
    BotCore.tele_bool = settings['tele_bool']
    BotCore.mode = 'multi'
    BotCore.counter_step = 20
    BotCore.max_waste_time = 10000
    TeleCore().start()

    start_event_parser('Название мероприятия. Мск. ',
                       'https://url.url/',
                       EventParser)
"""
