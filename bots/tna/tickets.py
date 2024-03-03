import re
import time

import aiohttp
from bs4 import BeautifulSoup


class Tickets:
    '''
    Занимае

    async def find_place_in_sector('sector', 'row', 'place') проверка доступности билета по сектору, ряду, месту
    async def update_sector('sector') обновить информацию о билетах в секторе
    '''
    def __init__(self, url):
        self.url = url #https://tna-tickets.ru/tickets/booking?id=14758
        self.cahe_time = 300 # 300 секунд = 5 минут, время которое должно пройти для повторного запроса
        self.start_time_epoch = time.time()
        self.event_id = url.split('=')[-1]
        self.access_token = None
        self.sectors_ids = {} # у каждого сектора свой ид
        self.main_structure = {} #здесь будут все доступные для покупки билеты (см структуру в update_sector)

        self.headers_sector =  {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,ru;q=0.8",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "referrer": "https://tna-tickets.ru/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, utf-8',
            'accept-language': 'ru,en;q=0.9',
            'connection': 'keep-alive',
            'host': 'tna-tickets.ru',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
            'sec-ch-ua-mobile': '?0',
            "sec-ch-ua-platform": "\"Linux\"",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            'x-requested-with': 'XMLHttpRequest'
        }


    def _check_time_passed(self, start_time):
        #проверяет, прошло ли более 5 минут с начальной точки отсчета
        current_time = time.time()
        return current_time - start_time > self.cahe_time 


    async def _load_access_token(self):
        '''Ищем токен для доступа к сайту https://tna-tickets.ru/
        '''
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'lxml')
                scripts = soup.find_all('script')
                function = [script for script in scripts if script.string and 'function' in script.string][0]
                function_text = function.text 
                self.access_token = re.search(r'[\w\d]+(?=\"\)\))', function_text)[0]
                return self.access_token
            

    async def _load_all_sectors(self)-> dict:
        '''загружаем ид всех секторов и возвращаем словарь
        '''

        url = f'https://api.tna-tickets.ru/api/v1/booking/{self.event_id}/sectors?access-token={self.access_token}&booking_ids'
        sectors_ids = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url,
                                   headers=self.headers_sector) as response:
                json = await response.json()
                all_sectors = json.get('result')
                for sector in all_sectors:
                    name = sector.get('name').split()[-1]
                    sector_id = sector.get('sector_id')
                    sectors_ids.setdefault(name, sector_id)
                return sectors_ids
            #sectors_ids = {'1': '1', '2': '394', '3': '881', '4': '1495', '5': '2045', '6': '2425', '7': '2901', '8': '3365',
            # '9': '3872', '10': '4354', '11': '4778', '12': '5152', '13': '5658', '14': '6137', '15': '6644', 
            #'16': '6977', '17': '7447', '18': '7945', '19': '8393', '20': '8851'} должен быть примерно таким
                    

    @staticmethod
    def _make_sector_row_seat(seat_name):
        #'Сектор 3A Ряд 3 Место 5'
        if not all(i in str(seat_name) for i in ('Сектор', 'Ряд', 'Место')):
            return False
        sector = re.search(r'(?<=Сектор) *\d+', seat_name)[0].strip()
        row = re.search(r'(?<=Ряд) *\d+', seat_name)[0].strip()
        place = re.search(r'(?<=Место) *\d+', seat_name)[0].strip()
        return sector, row, place  # ('3', '3', '5')       


    async def update_sector(self, sector_number:str):
        '''обновляем инфу о секторе

        Если все ок вернем True и
        создадим словрь self.main_structure
        self.main_structure = {'3<это сектор>': 
                    {'3<это ряд>': {'5<а это место в ряду>': {'seat_id': '893', 'seat_zone': '3', 'booking_id': '14758', 'name': 'Сектор 3A Ряд 3 Место 5'},
                                '11<это тоже место в ряду>': {'seat_id': '899', 'seat_zone': '3', 'booking_id': '14758', 'name': 'Сектор 3A Ряд 3 Место 11'}...}
            }
        
        если невозможно обновить вернем False
        '''

        if not self.access_token:
            access_token = await self._load_access_token()
            print(access_token, 'access_token')

        if sector_number not in self.sectors_ids:
            #загружаем ид всех секторов например сектор '2' имеет ид '394'
            self.sectors_ids = await self._load_all_sectors()

        sector_id = self.sectors_ids.get(sector_number)
        if not sector_id:
            return False
        
        self.main_structure[sector_number] = {}
            
        url = f'https://api.tna-tickets.ru/api/v1/booking/{self.event_id}/seats?access-token={self.access_token}&sector_id={sector_id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url,
                                   headers=self.headers_sector) as response:
                json = await response.json()
                all_seats_in_this_sector = json.get('result')
                for seat in all_seats_in_this_sector:
                    seat_id = seat.get("seat_id")
                    zone_id = seat.get('zone_id')
                    name = seat.get('name')
                    sector_row_seat = self._make_sector_row_seat(name)
                    if not sector_row_seat:
                        return False
                    sector, row, seat_ = sector_row_seat
                    ticket_to_buy = {'seat_id': seat_id, 'seat_zone': zone_id, 'booking_id': self.event_id,
                                     'name': name}
                    self.main_structure[sector_number].setdefault(row, {}).update(
                        {seat_:ticket_to_buy}
                    )
        return True


    async def find_place_in_sector(self, sector:str, row:str, place:str):
        '''Проверяем свободен ли сектор, ряд, место
        Пример использования Tickets.find_place_in_sector('20', '28', '9')

        Если место свободно вернет словарь:
       {'seat_id': '9284', 'seat_zone': '21', 'booking_id': '14758', 'name': 'Сектор 20B Ряд 28 Место 9'}

        Если недоступно вернет False
        '''

        if sector not in self.main_structure or self._check_time_passed(self.start_time_epoch):
            #если сектора нет в кэше, либо время последнего запроса более чем 5 минут, инициируем новую проверку этого сектора
            self.start_time_epoch = time.time()
            update_sector = await self.update_sector(sector)
        if sector in self.main_structure:
            all_rows = [ i for i in self.main_structure.get(sector, {})]
            if row in all_rows:
                all_seats = [ i for i in self.main_structure[sector].get(row, {})]
                if place in all_seats:
                    return self.main_structure[sector][row].get(place)
        return False