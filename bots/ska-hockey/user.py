import aiohttp
from aiohttp import BasicAuth
from bs4 import BeautifulSoup
from aiohttp.client_exceptions import ContentTypeError
from urllib.parse import urlencode


class User:
    def __init__(self, proxy:str, account:dict):
        ''' Аналог личного кабинета на сайте https://pass.ska.ru/
        В данный момент 1 юзер может купить 5 билетов

        Пример использования 
        1)Инициализация класса"
                proxy = "94.137.90.59:50100@mikheyev9:aXUbosImHR"
                account = {'login':'mikheyev9@gmail.com',
                           'password': 'Ai5F,;baB:rVf!8'} 
                user_1 = User(proxy=proxy,
                              account = account)

        2)Cоздать сессию 
                status_code = await user_1.make_session()

        3)Если status_code == 200:
            аутентифицировать пользователя:
                auth_status = await user_1.auth()

        4)Если auth_status == True:
            Добавить билеты в корзину:
                event_id = '1933'
                ticket_info = {'categoryId': '1',
                                'id': '572366',
                                'name': 'Сектор 615 Ряд 15 Место 118',
                                'orderId': '',
                                'price': '550.00',
                                'quant': '1'}
                post_status = await user_1.put_ticket_to_cart(event_id=event_id, 
                                                              ticket_info=ticket_info)

        5)При необходимости посмотреть какие билеты уже в корзине:
                print(self.all_tickets)

        6)Если в корзине есть билеты выводим на оплату:
                event_id = '1933'
                url_for_payment, account = await x.pay_tickets_from_cart(event_id)
                Получаем ссылка на оплату и аккуант                                                      
            

        *)async def make_session - создать сессию, вернет cатус код запроса на создание
        *)async def auth - аутентификация юзера если все ок вернет True иначе False
        *)async def close_session - закрыть сессию
        *)async def put_ticket_to_cart(event_id:ид мероприятия, ticket_info:билет)
            положить в корзину билет вернет True если OK иначе False

        *)async def pay_tickets_from_cart(event_id:ид мероприятия) - бронирование билетов в системе и
            создание ссылки на оплату. Вернет url оплаты и данные пользователя self.account если ОК,
            иначе raise AssertionError
        '''

        self.proxy_url, self.proxy_auth = self.make_proxy(proxy)
        self.proxy_status = None
        self.auth_status = None
        self.session = None
        self.cookies = {}

        self.account = account
        self.all_tickets = []

        self.headers_post =  {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,ru;q=0.8",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "Referer": "https://pass.ska.ru/en/auth/?back_domain=tickets&back_url=%2F",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    @staticmethod
    def make_proxy(proxy:str) -> tuple[str, BasicAuth]:
        #proxy = "94.137.90.59:50100@mikheyev9:aXUbosImHR"
        domain, user_info = proxy.split('@')
        proxy_url = f'http://{domain}'
        proxy_login, proxy_password = user_info.split(':')
        proxy_auth = BasicAuth(login=proxy_login, password=proxy_password)
        return proxy_url, proxy_auth

    async def _init_session(self) -> None:
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close_session(self) -> None:
        if self.session:
            await self.session.close()
            self.session = None


    async def make_session(self) -> str:
        '''Инициализация сессии и проверка доступности прокси,
           Если все ок, self.proxy_status == 200
        '''

        await self._init_session()
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,ru;q=0.8",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "Referer": "https://tickets.ska.ru/",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        url = 'https://pass.ska.ru/en/auth/?back_domain=tickets&back_url=%2F'
        try:
            async with self.session.get(url, headers=headers,
                                        proxy=self.proxy_url,
                                        proxy_auth=self.proxy_auth) as response:
                text = await response.text()
                self.CSRF = self._find_csrf(text)
                self.proxy_status = response.status
                print(self.CSRF, 'CSRF token')
                if not self.CSRF:
                    raise aiohttp.ClientConnectorError
                return response.status

        except aiohttp.ClientConnectorError as err:
            print(err)
            await self.close_session()
            return False
     
    @staticmethod
    def _find_csrf(text):
        soup = BeautifulSoup(text, 'lxml')
        meta = soup.find('meta', attrs={'name':'csrf-token'})
        if not meta:
            return False
        return meta.get('content')
    
    async def auth(self) -> bool:
        '''Авторизация пользователя в ситсеме покупки билетов
            Если все ок, self.auth_status == True

            self.account = { 'login': 'mikheyev9@gmail.com',
                            'password': 'Ai5F,;baB:rVf!8' }
        '''

        login = self.account['login']
        password = self.account['password']
        data = {
            '_csrf': self.CSRF,
            'login': login,
            'password': password,
            'auth_type': 'email',
            'send_submit': 'Y'
        }
        async with self.session.post(url='https://pass.ska.ru/en/auth/', 
                                     proxy=self.proxy_url,
                                     proxy_auth=self.proxy_auth,
                                     headers=self.headers_post, data=data) as response:
            if response.status == 200:
                self.auth_status = True
                print(response, self.auth_status, 'self.auth_status')
                return True
            return False


    async def put_ticket_to_cart(self, event_id:str, ticket_info:dict) -> bool:
        '''Положить билет в корзину пользователя
            Если все ок вернет True иначе False
        '''

        ticket = {
            'operation': 'add',
            'id': ticket_info['id'],
            'categoryId': ticket_info['categoryId'],
            'name': ticket_info['name'],
            'quant': ticket_info['quant'],
            'price': ticket_info['price'],
            'orderId': ''
        }

        async with self.session.post(url=f'https://tickets.ska.ru/cart/{event_id}', 
                                     headers=self.headers_post,
                                     proxy=self.proxy_url,
                                     proxy_auth=self.proxy_auth, 
                                     data=ticket) as response:
            try:
                response = await response.json()
            except ContentTypeError:
                return False
            if response.get('result', False) == True:
                self.all_tickets = response.get('list')
                return True
            elif response.get('result') == False:
                self.all_tickets = response.get('list')
                return False
            raise AssertionError(f'https://tickets.ska.ru/cart/{event_id} something went wrong')
    
    async def _create_order_to_pay(self, event_id:str) -> str | bool:
        '''Предварительный запрос на оплату
           Если все ок вернет id созданного платежа в их(СКА) системе
           Если нет вернет False'''

        pay_method = {'card': 'other'}
        async with self.session.get(url=f'https://tickets.ska.ru/create-order/{event_id}', 
                                    proxy=self.proxy_url,
                                    proxy_auth=self.proxy_auth,
                                    headers=self.headers_post) as response:
            try:
                json = await response.json()
            except ContentTypeError:
                return False
            if json.get('result'):
                return json['order']
            return False

    async def pay_tickets_from_cart(self, event_id:str) -> AssertionError | tuple[str, dict]:
            '''Создание запроса на оплату и получение ссылки от эквайринга
            '''
            
            create_order = await self._create_order_to_pay(event_id)
            if not create_order:
                raise AssertionError(f"Cannot pay this tickets {self.all_tickets}")
            pay_method = {'card': 'other'}

            async with self.session.post(url=f'https://tickets.ska.ru/pay-order/{create_order}', 
                                    proxy=self.proxy_url,
                                    proxy_auth=self.proxy_auth,
                                    headers=self.headers_post,
                                    data=pay_method) as response:
                
                text = await response.text()
                with open('Testing/TEST.html', 'w', encoding='utf-8') as f:
                    f.write(text)
                soup = BeautifulSoup(text, 'lxml')
                form_gazprombank = soup.find('form', attrs={'action':"https://www.pga.gazprombank.ru:443/pages/"})
                lang = form_gazprombank.find('input', attrs={'name':'lang'}).get('value')
                merch_id = form_gazprombank.find('input', attrs={'name':'merch_id'}).get('value')
                back_url_s = form_gazprombank.find('input', attrs={'name':'back_url_s'}).get('value')
                back_url_f = form_gazprombank.find('input', attrs={'name':'back_url_f'}).get('value')
                order_id = form_gazprombank.find('input', attrs={'name':'o.order_id'}).get('value')
                tickets_count = form_gazprombank.find('input', attrs={'name':'o.tickets_count'}).get('value')
                action_id = form_gazprombank.find('input', attrs={'name':'o.action_id'}).get('value')
                SUBMIT = form_gazprombank.find('input', attrs={'name':'SUBMIT'}).get('value')
                
                

                url = "https://www.pga.gazprombank.ru:443/pages/"
                params = {
                    "lang": lang,
                    "merch_id": merch_id,
                    "back_url_s": back_url_s,
                    "back_url_f": back_url_f,
                    "o.order_id": order_id,
                    "o.tickets_count": tickets_count,
                    "o.action_id": action_id,
                    "SUBMIT": SUBMIT
                }
                encoded_params = urlencode(params)
                full_url = f"https://www.pga.gazprombank.ru:443/pages/?{encoded_params}"

                return full_url, self.account