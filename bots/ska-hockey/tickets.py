import re
import time

import aiohttp
from bs4 import BeautifulSoup


class Tickets:
    '''
    async def find_place_in_sector(sector, row, place) если ОК вернет

    если место не свободно вернет  False
    '''
    def __init__(self, url):
        self.url = url #'https://tickets.ska.ru/view-available-zones/1928'
        self.cahe_time = 300  # 300 секунд = 5 минут, время которое должно пройти для повторного запроса

        self.start_time_epoch = time.time()
        self.all_free_sectors = {} #смотри _update_all_free_sectors
        self.all_tickets_structure = {} # cм _update_rows_seats_in_sector
        self.all_prices_id = {} # см _update_rows_seats_in_sector

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru,en;q=0.9',
            'cache-control': 'max-age=0',
            'connection': 'keep-alive',
            'host': 'tickets.ska.ru',
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            'sec-ch-ua-mobile': '?0',
            "sec-ch-ua-platform": "\"Linux\"",
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def _check_time_passed(self, start_time:int) -> bool:
        #проверяет, прошло ли более 5 минут с начальной точки отсчета
        current_time = time.time()
        return current_time - start_time > self.cahe_time
        
    async def _update_all_free_sectors(self) -> dict:
        '''
        обновлет информацию обо всех доступных сектрах в self.all_free_sectors
        {'202': {'url': 'https://tickets.ska.ru/seats-list/2062/550733'},
         '203': {'url': 'https://tickets.ska.ru/seats-list/2062/551226'},
         '204': {'url': 'https://tickets.ska.ru/seats-list/2062/551861'}, ...
         }

        '''
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=self.headers) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'lxml')

                text_js = soup.find('div', class_='wrp-main').find('script').text
                no_render_data = text_js[text_js.index('['):text_js.index('];')+1]
                dict_data = eval(no_render_data.replace('null', 'None'))
                #dict_data=[{'id': '560617', 'name': 304, 'quant': '31', 'zoneId': '-99999', 'zoneTypeId': '100',
                #           'price': [1200, 2400], 'url': 'https://tickets.ska.ru/seats-list/1928/560617'}, ... ]

                all_sectors_structure = {}

                for sectors in dict_data:
                        sector = sectors.get('name')
                        if sector:
                            sector_id = sectors.get('id')
                            url_split = self.url.split("/")
                            url_sector = f'seats-list/{url_split[-1]}/{sector_id}'
                            url_to_sector = '/'.join(url_split[:-2]) + '/' + url_sector
                            sectors.update({'url':url_to_sector})
                            #print(url_to_sector)
                            all_sectors_structure.setdefault(str(sector), {}).update({
                                                            'url':url_to_sector
                                                            })

                self.all_free_sectors = all_sectors_structure
                return dict_data
    
    async def _update_rows_seats_in_sector(self, sector_name: str) -> bool:
        '''
        обновление всех свободых мест в определенном секторе
        устанавливает
        self.all_tickets_structure
            {'604': (это сектор)
                {'4': (это ряд)
                    {'3': (это место) {'categoryId': '1',
                                    'id': '565455',
                                    'name': 'Сектор 604 Ряд 4 Место 3',
                                    'orderId': '',
                                    'price': '1590.00',
                                    'quant': '1'},
                   '103': (это место){'categoryId': '1',
                                    'id': '565470',
                                    'name': 'Сектор 604 Ряд 4 Место 103',
                                    'orderId': '',
                                    'price': '1590.00',
                                    'quant': '1'},
                                    ...
                                    }}}
        self.all_prices_id
         {'1': {'341': '1590.00', '293': '2290.00', '294': '2190.00', '295': '2390.00'},
         '21': {'341': '795.00', '293': '1145.00', '294': '1095.00', '295': '1195.00'},...}
        '''
        if sector_name not in self.all_free_sectors:
            await self._update_all_free_sectors()
            #print(self.all_free_sectors, 'all_free_sectors')
            if sector_name not in self.all_free_sectors:
                self.all_tickets_structure[sector_name] = {}
                print(f"Sector:{sector_name} isnt availible")
                return False
        url = self.all_free_sectors[sector_name]['url']
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                json = await response.json()
                prices = json.get('prices')
                for price in prices:
                    self.all_prices_id.setdefault(price["categoryId"], {}).update({
                        price["pricezoneId"]: price['value']
                    })
                seats = json.get('seats')
                if len(seats) <= 0:
                    return False
                first_blood = 1 # При первом проходе очищаются все места для этого сектора, чтобы обновить информацию о наличии
                for seat in seats:
                    categoryId = seat.get('quant')
                    id = seat.get('id')
                    name = seat.get('name')
                    price_zone = seat.get('pricezoneId')
                    price = self.all_prices_id[categoryId].get(price_zone)
                    sector_row_place = self._parsing_seat(name)
                    if sector_row_place:
                        sector, row, place = sector_row_place
                        self.all_tickets_structure.setdefault(sector, {})
                        if first_blood:
                            self.all_tickets_structure[sector] = {row: {}}
                            first_blood = 0
                        else:
                            self.all_tickets_structure[sector].setdefault(row, {})
                        self.all_tickets_structure[sector][row].setdefault(place, {}).update({
                                        'categoryId': categoryId,
                                        'id': id,
                                        'name': name,
                                        'orderId': '',
                                        'price': price,
                                        'quant': '1'
                        })
        return True
                    

    @staticmethod   
    def _parsing_seat(seat_name:str) -> tuple[str,str,str] | bool:
        #Сектор 304 Ряд 22 Место 107
        if not all(i in seat_name  for i in ('Сектор', 'Ряд', 'Место')):
            return False
        sector = re.search(r'(?<=Сектор) *\d+', seat_name)[0].strip()
        row = re.search(r'(?<=Ряд) *\d+', seat_name)[0].strip()
        place = re.search(r'(?<=Место) *\d+', seat_name)[0].strip()
        return sector, row, place         


    async def find_place_in_sector(self, sector, row, place) -> dict | bool:
        if sector not in self.all_tickets_structure or self._check_time_passed(self.start_time_epoch):
            self.start_time_epoch = time.time()
            update_sector = await self._update_rows_seats_in_sector(sector)
        if sector in self.all_tickets_structure:
            all_rows = [i for i in self.all_tickets_structure.get(sector, {})]
            if row in all_rows:
                all_seats = [i for i in self.all_tickets_structure[sector].get(row, {})]
                if place in all_seats:
                    return self.all_tickets_structure[sector][row].get(place)
        return False