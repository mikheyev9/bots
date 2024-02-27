import asyncio
import os
import json

from user import User
from tickets import Tickets

class Main:
    def __init__(self, event_url:str):
        self.event_url = event_url
        self.Tickets = Tickets(event_url)
        self.event_id = event_url.split('=')[-1]
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.user_accounts = self.load_accounts()
        self.proxies = self.load_proxies()
        self.need_tickets = self.dict_to_tuples(self.load_need_tickets())

        self.tickets_queue = asyncio.Queue()


    @staticmethod
    def dict_to_tuples(dict_data):
        tuples = []
        for outer_key, inner_dict in dict_data.items():
            for inner_key, value in inner_dict.items():
                for item in value:
                    tuples.append((outer_key, inner_key, str(item)))
        return tuples
    

    def load_accounts(self):
        path = os.path.join(self.current_directory, 'accounts.json')
        with open(path, 'r') as file:
            user_accounts = json.load(file)
            return user_accounts
        
        
    def load_proxies(self):
        path = os.path.join(self.current_directory, 'proxies.json')
        with open(path, 'r') as file:
            proxies = json.load(file)
            return proxies
        
        
    def load_need_tickets(self):
        path = os.path.join(self.current_directory, 'need_tikets.json')
        with open(path, 'r') as file:
            need_tikets = json.load(file)
            return need_tikets
        
    async def main_search_availible_tickets(self):
        semaphore = asyncio.Semaphore(5)
        for sector_row_place in self.need_tickets:
            task = self._put_to_tickets_queue(sector_row_place, semaphore)
            await task
    

    async def _put_to_tickets_queue(self, sector_row_place: tuple,
                                  semaphore: asyncio.Semaphore):
        async with semaphore:
            sector, row, place = sector_row_place
            is_place_availible = await self.Tickets.find_place_in_sector(sector, row, place)
            print(is_place_availible, sector_row_place, 'availibility of place')
            if is_place_availible:
                await self.tickets_queue.put((is_place_availible, sector, row, place))
                return True
            return False
        
    async def _monitor_tickets_queue(self, semaphore):
        lock = asyncio.Lock()
        while True:
            # Ожидаем получения 5 билетов из очереди
            tickets_batch = []
            for _ in range(4):
                ticket = await self.tickets_queue.get()
                tickets_batch.append(ticket)
            
            async def process_with_error_handling(tickets_batch_, lock_):
                try:
                    await self.process_tickets_batch(tickets_batch_, lock_)
                except Exception as ex:
                    print(ex)  # Обработка исключения непосредственно в задаче
            # Создаем и запускаем задачу для обработки пакета билетов

            async with semaphore:
                asyncio.create_task(process_with_error_handling(tickets_batch, lock))


    async def process_tickets_batch(self, tickets_batch, lock):
        user = await self._auth_account()
        try:
            if user:
                box = []
                for ticket_info in tickets_batch:
                    ticket_info_, sector, row, place = ticket_info
                    #ticket_info_ = {'seat_id': "901", 'seat_zone': "3", 'booking_id': "14758",
                    #                   'name': Сектор 3A Ряд 20 Место 7 }
                    resault_of_put = await user.put_tickets_to_basket(seat_id=ticket_info_['seat_id'],
                                                                      seat_zone=ticket_info_['seat_zone'],
                                                                      url=self.event_url)
                    print(resault_of_put,  ticket_info_.get('name'))
                    if resault_of_put:
                        box.append(ticket_info_.get('name'))
                #box_resaults = await asyncio.gather(*box, return_exceptions=True)  
                if len(box) > 0:
                    url_for_payment, account = await user.create_order()
                    async with lock:
                        path = os.path.join(self.current_directory, 'tickets.txt')
                        with open(path, 'a', encoding='utf-8') as file:
                            file.write(f"{url_for_payment}\n{account}\n{box}\n\n\n" )
                    print(url_for_payment, account)       
        except Exception as ex:
            print(ex)
        finally:
            if user:
                await user.close_session()

    async def _auth_account(self):
        if len(self.user_accounts) <= 0:
            print('Out of users!')
            return False
        user_accounts = self.user_accounts.pop()
        if len(self.proxies) <= 0:
            print('Out of proxies')
            return False
        proxy = self.proxies.pop()
        user = User(proxy, user_accounts)
        status_code = await user.auth()
        if status_code != 200:
            self.user_accounts.append(user_accounts)
            return False
        return user
    
    async def main(self):
        # Создаем семафор для ограничения количества одновременно выполняемых задач
        semaphore = asyncio.Semaphore(10)

        # Запускаем асинхронную функцию для добавления билетов в очередь
        add_tickets_task = asyncio.create_task(self.main_search_availible_tickets())
        print('add_tickets_task run')
        # Запускаем мониторинг очереди
        monitor_tickets_task = asyncio.create_task(self._monitor_tickets_queue(semaphore))
        print('monitor_tickets_task run')
        await asyncio.gather(add_tickets_task, monitor_tickets_task)