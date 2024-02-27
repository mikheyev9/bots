import aiohttp
from aiohttp import BasicAuth
import re

from bs4 import BeautifulSoup


class User:
    def __init__(self, proxy:str, account:dict):
        self.proxy_url, self.proxy_auth = self.make_proxy(proxy)
      
        self.session = None
        self.access_token = None
        self.user_token = None
        self.url_login = None
        self.basket = []
        self.cookies = {}

        self.account = account
        self.all_tickets = []

        self.headers =  {
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


    async def _make_login_page(self, url):
        await self._init_session()

        async with self.session.get(url, headers=self.headers,
                                    proxy=self.proxy_url,
                                    proxy_auth=self.proxy_auth) as response:
            text = await response.text()
            soup = BeautifulSoup(text, 'lxml')
            scripts = soup.find_all('script')
            function = [script for script in scripts if script.string and 'function' in script.string][0]
            function_text = function.text 
            access_token = re.search(r'[\w\d]+(?=\"\)\))', function_text)[0]
            print(access_token)
            return access_token
            

    async def auth(self, url='https://tna-tickets.ru/tickets/login'):
        try:
            self.access_token = await self._make_login_page(url)
            self.url_login = f'https://api.tna-tickets.ru/api/v1/user/login?access-token={self.access_token}'

            async with self.session.post(self.url_login, headers=self.headers,
                            data=self.account,
                            proxy=self.proxy_url,
                            proxy_auth=self.proxy_auth) as response:
                print(response.status)
                response_text = await response.text()
                print(response_text)
                response_json = await response.json()
                self.user_token = response_json.get('result')['user_token']
                return response.status
        except Exception:
            return False
        

    @staticmethod
    def set_url_with_sectors(url):
        #https://tna-tickets.ru/tickets/booking?id=14758
        booking_id = url.split('=')[-1]
        return booking_id


    async def put_tickets_to_basket(self, seat_id:str, seat_zone:str, url:str):
        booking_id = self.set_url_with_sectors(url)
        ticket_to_buy = {'seat_id': seat_id,
                        'seat_zone': seat_zone,
                        'booking_id': booking_id}
        url = f'https://api.tna-tickets.ru/api/v1/booking/seat-reserve?access-token={self.access_token}&user_token={self.user_token}'
        async with self.session.post(url=url, 
                                    headers=self.headers,
                                    data=ticket_to_buy,
                                    proxy=self.proxy_url,
                                    proxy_auth=self.proxy_auth) as response:
            print(response.status)
            response_json = await response.json()
            result = response_json.get('status')
            tickets = response_json.get('result')
            if result and tickets:
                self.basket = tickets
            return response, response_json
    

    async def create_order(self):
        url = f'https://api.tna-tickets.ru/api/v1/order/create?access-token={self.access_token}&user_token={self.user_token}&promocode'
        headers_lock = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,ru;q=0.8",
            "content-type": "application/json",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        async with self.session.post(url=url, 
                                    headers=headers_lock,
                                    proxy=self.proxy_url,
                                    proxy_auth=self.proxy_auth) as response:
            print(response.status, 'create order status')
            json = await response.json()
            if json:
                status = json.get('status')
                result = json.get('result',{}).get("payment_link")
                return result, self.account
            return None, None