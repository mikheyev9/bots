import re
import time

import aiohttp
from bs4 import BeautifulSoup


class Tickets:
    def __init__(self, url):
        self.url = url #https://tna-tickets.ru/tickets/booking?id=14758
        self.start_time_epoch = time.time()
        self.event_id = url.split('=')[-1]
        self.access_token = None
        self.sectors_ids = {}
        self.main_structure = {}

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


    @staticmethod
    def check_time_passed(start_time):
        #проверяет, прошло ли более 5 минут с начальной точки отсчета
        current_time = time.time()
        return current_time - start_time > 300  # 300 секунд = 5 минут


    async def load_access_token(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'lxml')
                scripts = soup.find_all('script')
                function = [script for script in scripts if script.string and 'function' in script.string][0]
                function_text = function.text 
                self.access_token = re.search(r'[\w\d]+(?=\"\)\))', function_text)[0]
                return self.access_token
            

    async def _load_all_sectors(self):
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
                    
    @staticmethod
    def _make_sector_row_seat(seat_name):
        #'Сектор 3A Ряд 3 Место 5'
        if not all(i in str(seat_name) for i in ('Сектор', 'Ряд', 'Место')):
            return False
        sector = re.search(r'(?<=Сектор) *\d+', seat_name)[0].strip()
        row = re.search(r'(?<=Ряд) *\d+', seat_name)[0].strip()
        place = re.search(r'(?<=Место) *\d+', seat_name)[0].strip()
        return sector, row, place         

    async def update_sector(self, sector_number:str):
        if not self.access_token:
            access_token = await self.load_access_token()
            print(access_token, 'access_token')
        if sector_number not in self.sectors_ids:
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
        if sector not in self.main_structure or self.check_time_passed(self.start_time_epoch):
            self.start_time_epoch = time.time()
            update_sector = await self.update_sector(sector)
            print(update_sector, 'update_sector')
        if sector in self.main_structure:
            all_rows = [ i for i in self.main_structure.get(sector, {})]
            if row in all_rows:
                all_seats = [ i for i in self.main_structure[sector].get(row, {})]
                if place in all_seats:
                    return self.main_structure[sector][row].get(place)
        return False