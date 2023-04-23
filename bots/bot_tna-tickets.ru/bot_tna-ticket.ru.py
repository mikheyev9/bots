from loguru import logger

from cores_src.bot_sample_server import *
from event_bot import EventParser
import authorization

BotCore.tele_bool = settings['tele_bool']
BotCore.release = True
BotCore.proxy_centralized = True
TEST = False


class ObserverBot(ObserverBotSample):

    def __init__(self, *init_args, **from_needed_events):
        super().__init__(*init_args, **from_needed_events)
        self.from_observer = None
        self.event_id = double_split(self.URL, 'tickets/', '/')

    def before_body(self):
        self.account = accounts.get()
        self.from_observer = {
            'account': self.account,
            'event_id': self.event_id
        }

    def get_request(self):
        url = f'https://api.tna-tickets.ru/api/v1/booking/{self.event_id}' \
              f'/sectors?access-token={api_token}'
        headers = {
           'accept': 'application/json, text/plain, */*',
           'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
           'cache-control': 'no-cache',
           'origin': 'https://www.ak-bars.ru',
           'pragma': 'no-cache',
           'referer': f'https://www.ak-bars.ru/tickets/{self.event_id}',
           'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"',
           'sec-fetch-dest': 'empty',
           'sec-fetch-mode': 'cors',
           'sec-fetch-site': 'cross-site',
           'user-agent': self.user_agent,
        }
        if TEST:
            return [
                {
                    "sector_id": "394",
                    "name": "Сектор 2",
                    "quant": "8",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S02.jpg",
                },
                {
                    "sector_id": "881",
                    "name": "Сектор 3",
                    "quant": "4",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S03.jpg",
                },
                {
                    "sector_id": "2045",
                    "name": "Сектор 5",
                    "quant": "4",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S05.jpg",
                },
                {
                    "sector_id": "2425",
                    "name": "Сектор 6",
                    "quant": "46",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S06.jpg",
                },
                {
                    "sector_id": "2901",
                    "name": "Сектор 7",
                    "quant": "4",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S07.jpg",
                },
                {
                    "sector_id": "3365",
                    "name": "Сектор 8",
                    "quant": "10",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S08.jpg",
                },
                {
                    "sector_id": "3872",
                    "name": "Сектор 9",
                    "quant": "2",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S09.jpg",
                },
                {
                    "sector_id": "4354",
                    "name": "Сектор 10",
                    "quant": "13",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S10.jpg",
                },
                {
                    "sector_id": "4778",
                    "name": "Сектор 11",
                    "quant": "20",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S11.jpg",
                },
                {
                    "sector_id": "5152",
                    "name": "Сектор 12",
                    "quant": "25",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S12.jpg",
                },
                {
                    "sector_id": "5658",
                    "name": "Сектор 13",
                    "quant": "12",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S13.jpg",
                },
                {
                    "sector_id": "6644",
                    "name": "Сектор 15",
                    "quant": "22",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S15.jpg",
                },
                {
                    "sector_id": "6977",
                    "name": "Сектор 16",
                    "quant": "6",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S16.jpg",
                },
                {
                    "sector_id": "7945",
                    "name": "Сектор 18",
                    "quant": "21",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S18.jpg",
                },
                {
                    "sector_id": "8393",
                    "name": "Сектор 19",
                    "quant": "19",
                    "zone_id": "-99999",
                    "zonetype_id": "100",
                    "seattype_id": "-99999",
                    "seatclass_id": "20",
                    "thumb": "https://api.tna-tickets.ru/storage/public/sectors/S19.jpg",
                },
            ]
        r = self.account.get(url, headers=headers)
        status = r.json()['status']
        if status != 200:
            raise RuntimeError(f'Status is wrong in ObserverBot {status}')
        if not r.json()['result']:
            raise RuntimeError('There is no any sector on a sector request')
        return r.json()['result']

    def get_sectors(self):
        countable = False
        raw_sectors = self.get_request()

        limit = 5
        for sector in raw_sectors:
            sector['limit'] = limit
        return raw_sectors, countable


class SectorGrabber(SectorGrabberSample):
    def __init__(self, *init_args):
        super().__init__(*init_args)

    def tickets_request(self):
        account = self.from_observer['account']
        event_id = self.from_observer['event_id']
        sector_id = self.sector_data['sector_id']
        url = f'https://api.tna-tickets.ru/api/v1/booking/{event_id}/seats?access-token' \
              f'={api_token}&sector_id={sector_id}'
        headers = {
           'accept': 'application/json, text/plain, */*',
           'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
           'cache-control': 'no-cache',
           'origin': 'https://www.ak-bars.ru',
           'pragma': 'no-cache',
           'referer': f'https://www.ak-bars.ru/tickets/{event_id}',
           'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"',
           'sec-fetch-dest': 'empty',
           'sec-fetch-mode': 'cors',
           'sec-fetch-site': 'cross-site',
           'user-agent': self.user_agent,
        }
        if TEST:
            if sector_id == '394':
                return [
                    {
                        "seat_id": "6979",
                        "name": "Сектор 16A Ряд 1 Место 1",
                        "quant": "1",
                        "color": "16777215",
                        "zone_id": "3",
                        "zonetype_id": "100",
                    },
                    {
                        "seat_id": "6999",
                        "name": "Сектор 16A Ряд 2 Место 1",
                        "quant": "1",
                        "color": "16777215",
                        "zone_id": "3",
                        "zonetype_id": "100",
                    }
                ]
        r = account.get(url, headers=headers)
        return r.json()['result']

    def get_tickets(self):
        tickets = self.tickets_request()
        a_tickets = []
        for ticket in tickets:
            ticket['row'] = double_split(ticket['name'], 'Ряд ', ' ')
            ticket['seat'] = double_split(ticket['name'], 'Место ', ' ')
            if ticket['zone_id'] in ['25', '59']:
                print(yellow(f'Skipping tickets with price zone {ticket["zone_id"]}'))
                continue
            a_tickets.append(ticket)
        return a_tickets


class OrderBot(OrderBotSample):
    def __init__(self, *init_args, **init_kwargs):
        super().__init__(*init_args, **init_kwargs)
        self.price_zones = None

    def after_get_q(self):
        self.account = self.accounts.get()
        counter = 0
        while self.from_observer['event_id'] in self.account.bought:
            counter += 1
            if counter == 10:
                raise RuntimeError('Could not get account after 10 tries')
            self.account = self.accounts.change(self.account)
        self.price_zones = self.get_price_zones()

    def get_price_zones(self):
        event_id = self.from_observer['event_id']
        url = f'https://api.tna-tickets.ru/api/v1/booking/{event_id}/seats-price?access-token' \
              f'={api_token}&sector_id={self.sector_data["sector_id"]}'
        logger.info(url)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
            'cache-control': 'no-cache',
            'origin': 'https://www.ak-bars.ru',
            'pragma': 'no-cache',
            'referer': f'https://www.ak-bars.ru/tickets/{event_id}',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': self.user_agent,
        }
        if TEST:
            price_zones = [
                {
                    "id": "54846",
                    "category_id": "2",
                    "zone_id": "2",
                    "zonetype_id": "100",
                    "price": "3850.00",
                    "discount": "0.00",
                    "zonename": "Первая",
                    "categoryname": "Общий",
                    "zonefullname": "Первая",
                    "categoryfullname": "Общий",
                    "color": "16776960",
                },
                {
                    "id": "54826",
                    "category_id": "2",
                    "zone_id": "193",
                    "zonetype_id": "100",
                    "price": "2300.00",
                    "discount": "0.00",
                    "zonename": "Двадцать шестая",
                    "categoryname": "Общий",
                    "zonefullname": "Двадцать шестая",
                    "categoryfullname": "Общий",
                    "color": "12615935",
                },
                {
                    "id": "54849",
                    "category_id": "2",
                    "zone_id": "3",
                    "zonetype_id": "100",
                    "price": "3700.00",
                    "discount": "0.00",
                    "zonename": "Вторая",
                    "categoryname": "Общий",
                    "zonefullname": "Вторая",
                    "categoryfullname": "Общий",
                    "color": "65535",
                },
                {
                    "id": "54851",
                    "category_id": "2",
                    "zone_id": "16",
                    "zonetype_id": "100",
                    "price": "2900.00",
                    "discount": "0.00",
                    "zonename": "Третья",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "11468718",
                },
                {
                    "id": "54854",
                    "category_id": "2",
                    "zone_id": "17",
                    "zonetype_id": "100",
                    "price": "2750.00",
                    "discount": "0.00",
                    "zonename": "Четвертая",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "32768",
                },
                {
                    "id": "54855",
                    "category_id": "2",
                    "zone_id": "18",
                    "zonetype_id": "100",
                    "price": "2000.00",
                    "discount": "0.00",
                    "zonename": "Пятая",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "16711680",
                },
                {
                    "id": "54857",
                    "category_id": "2",
                    "zone_id": "19",
                    "zonetype_id": "100",
                    "price": "1800.00",
                    "discount": "0.00",
                    "zonename": "Шестая",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "8454143",
                },
                {
                    "id": "54859",
                    "category_id": "2",
                    "zone_id": "20",
                    "zonetype_id": "100",
                    "price": "1750.00",
                    "discount": "0.00",
                    "zonename": "Седьмая",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "4227327",
                },
                {
                    "id": "54861",
                    "category_id": "2",
                    "zone_id": "21",
                    "zonetype_id": "100",
                    "price": "1350.00",
                    "discount": "0.00",
                    "zonename": "Восьмая",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "16711935",
                },
                {
                    "id": "54863",
                    "category_id": "2",
                    "zone_id": "22",
                    "zonetype_id": "100",
                    "price": "1350.00",
                    "discount": "0.00",
                    "zonename": "Девятая",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "8388736",
                },
                {
                    "id": "54865",
                    "category_id": "2",
                    "zone_id": "23",
                    "zonetype_id": "100",
                    "price": "1300.00",
                    "discount": "0.00",
                    "zonename": "Десятая ",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "8388863",
                },
                {
                    "id": "54848",
                    "category_id": "2",
                    "zone_id": "43",
                    "zonetype_id": "100",
                    "price": "4000.00",
                    "discount": "0.00",
                    "zonename": "Первая (центр)",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "17919",
                },
                {
                    "id": "54850",
                    "category_id": "2",
                    "zone_id": "44",
                    "zonetype_id": "100",
                    "price": "3850.00",
                    "discount": "0.00",
                    "zonename": "Вторая (центр)",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "13990699",
                },
                {
                    "id": "54853",
                    "category_id": "2",
                    "zone_id": "71",
                    "zonetype_id": "100",
                    "price": "2900.00",
                    "discount": "0.00",
                    "zonename": "Четвертая (центр)",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "12639424",
                },
                {
                    "id": "54856",
                    "category_id": "2",
                    "zone_id": "70",
                    "zonetype_id": "100",
                    "price": "2100.00",
                    "discount": "0.00",
                    "zonename": "Пятая (центр)",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "255",
                },
                {
                    "id": "54858",
                    "category_id": "2",
                    "zone_id": "72",
                    "zonetype_id": "100",
                    "price": "1900.00",
                    "discount": "0.00",
                    "zonename": "Шестая (центр)",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "32896",
                },
                {
                    "id": "54862",
                    "category_id": "2",
                    "zone_id": "73",
                    "zonetype_id": "100",
                    "price": "1450.00",
                    "discount": "0.00",
                    "zonename": "Восьмая (центр)",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "33023",
                },
                {
                    "id": "54860",
                    "category_id": "2",
                    "zone_id": "74",
                    "zonetype_id": "100",
                    "price": "1850.00",
                    "discount": "0.00",
                    "zonename": "Седьмая (центр)",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "128",
                },
                {
                    "id": "54864",
                    "category_id": "2",
                    "zone_id": "75",
                    "zonetype_id": "100",
                    "price": "1450.00",
                    "discount": "0.00",
                    "zonename": "Девятая (центр)",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "8421376",
                },
                {
                    "id": "54866",
                    "category_id": "2",
                    "zone_id": "77",
                    "zonetype_id": "100",
                    "price": "1350.00",
                    "discount": "0.00",
                    "zonename": "Десятая (центр)",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "42495",
                },
                {
                    "id": "54852",
                    "category_id": "2",
                    "zone_id": "78",
                    "zonetype_id": "100",
                    "price": "3050.00",
                    "discount": "0.00",
                    "zonename": "Третья (центр)",
                    "categoryname": "Общий",
                    "categoryfullname": "Общий",
                    "color": "12695295",
                },
                {
                    "id": "54824",
                    "category_id": "2",
                    "zone_id": "79",
                    "zonetype_id": "100",
                    "price": "3350.00",
                    "discount": "0.00",
                    "zonename": "Двадцать четвертая",
                    "categoryname": "Общий",
                    "zonefullname": "Двадцать четвертая",
                    "categoryfullname": "Общий",
                    "color": "8388736",
                },
                {
                    "id": "54825",
                    "category_id": "2",
                    "zone_id": "80",
                    "zonetype_id": "100",
                    "price": "3500.00",
                    "discount": "0.00",
                    "zonename": "Двадцать пятая",
                    "categoryname": "Общий",
                    "zonefullname": "Двадцать пятая",
                    "categoryfullname": "Общий",
                    "color": "32768",
                },
            ]
        else:
            r = self.account.get(url, headers=headers)
            price_zones = r.json()['result']
        zones_dict = {zone['zone_id']: zone for zone in price_zones}
        return zones_dict

    def add_to_cart(self, ticket):
        url = f'https://api.tna-tickets.ru/api/v1/booking/seat-reserve?access-token=' \
              f'{api_token}&user_token={self.account.data["user_token"]}'
        logger.info(url)
        event_id = self.from_observer['event_id']
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
            'cache-control': 'no-cache',
            'content-length': '69',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.ak-bars.ru',
            'pragma': 'no-cache',
            'referer': f'https://www.ak-bars.ru/tickets/{event_id}',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': self.user_agent,
        }
        price_zone = ticket['zone_id']
        if price_zone not in self.price_zones:
            all_zones = list(self.price_zones.keys())
            raise RuntimeError(f'No price_zone {price_zone} in {all_zones}')
        current_zone = self.price_zones[price_zone]
        data = {
           'seat_id': ticket['seat_id'],
           'seat_zone': ticket['zonetype_id'],
           'booking_id': self.from_observer['event_id'],
           'booking_ids': '',
           'category_id': current_zone['category_id']
        }
        logger.info(data)
        r = self.account.post(url, data=data, headers=headers)
        jsoned = r.json()
        status = jsoned['status']

        if status != 200:
            logger.warning(f'add_to_cart status {status}')
            return
        seat_ids = [ticket['seat_id'] for ticket in jsoned['result'] if 'seat_id' in ticket]
        if ticket['seat_id'] not in seat_ids:
            logger.warning(f'adding seat was not found in the cart')
        else:
            description = ticket['name']
            row = double_split(description, 'Ряд ', ' ')
            seat = double_split(description, 'Место ', ' ')
            cost = current_zone['price']
            ticket_descr = (f'Ряд {row}, '
                            f'Место {seat}, '
                            f'Стоимость {cost} руб')
            return ticket_descr

    def create_order(self):
        # Input data:
        #   self.from_needed_events - input data for event from needed.py
        #   self.from_observer - specific data for whole event
        #   self.sector_data - entire data on sector
        #   self.tickets_pack - all tickets are here
        #   self.ticket_descrs - all succeeded ticket descriptions
        event_id = self.from_observer['event_id']
        url = f'https://api.tna-tickets.ru/api/v1/order/create?access-token=' \
              f'{api_token}&user_token={self.account.data["user_token"]}'
        logger.info(url)
        print(self.account)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
            'cache-control': 'no-cache',
            'content-length': '10',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.ak-bars.ru',
            'pragma': 'no-cache',
            'referer': f'https://www.ak-bars.ru/tickets/{event_id}',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': self.user_agent,
        }
        data = {
            'promocode': '',
        }
        r = self.account.post(url, headers=headers, data=data)
        if 'result' not in r.json():
            self.bprint(f'Create order error: {r.text}', color=Fore.RED)
        checkout_data = r.json()['result']
        order_id = checkout_data['order_id']
        payment_link = checkout_data['payment_link']

        url = f'https://api.tna-tickets.ru/api/v1/order?access-token=' \
              f'{api_token}&user_token={self.account.data["user_token"]}'
        logger.info(url)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
            'cache-control': 'no-cache',
            'origin': 'https://www.ak-bars.ru',
            'pragma': 'no-cache',
            'referer': f'https://www.ak-bars.ru/tickets/orders/{order_id}',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': self.user_agent,
        }
        r = self.account.get(url, headers=headers)

        url = f'https://api.tna-tickets.ru/api/v1/order/{order_id}?access-token=' \
              f'{api_token}&user_token={self.account.data["user_token"]}'
        logger.info(url)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
            'cache-control': 'no-cache',
            'origin': 'https://www.ak-bars.ru',
            'pragma': 'no-cache',
            'referer': f'https://www.ak-bars.ru/tickets/orders/{order_id}',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': self.user_agent,
        }
        r = self.account.get(url, headers=headers)

        """logger.info(payment_link)
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,im'
                      'age/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': f'https://www.ak-bars.ru/tickets/orders/{order_id}',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent,
        }
        r = self.account.get(payment_link, headers=headers, allow_redirects=True)
        print(r.text)
        print(r.url)"""
        return payment_link


def get_api_token(session):
    url = 'https://www.ak-bars.ru/'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,im'
                  'age/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
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

    script_url = 'https://www.ak-bars.ru' + script_dirs[-2]
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
    accounts = start_accounts_queue(authorization.TNAQueue, api_token=api_token,
                                    reauthorize=True)

    # Defining global variables
    tickets_q = Queue()
    sectors_q = Queue()

    # Starting buying threads
    manager_socket = start_buying_bots(ObserverBot, SectorGrabber,
                                       OrderBot, sectors_q, tickets_q,
                                       accounts_q=accounts)
    start_event_parser('Ак-Барс. Мск. ',
                       'https://www.ak-bars.ru/tickets/',
                       EventParser, api_token=api_token)
    while True:
        input()
        monitor(SectorGrabber, OrderBot, manager_socket, monitor_q=accounts)
