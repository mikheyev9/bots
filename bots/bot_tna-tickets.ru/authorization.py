import requests
from loguru import logger
from requests.exceptions import SSLError
from requests.utils import dict_from_cookiejar
from urllib3 import HTTPSConnectionPool

from cores_src import authorize
from cores_src.vis import *
from cores_src.cores import *

ERRORS = ['500 Internal Server Error', '504 Gateway Time-out']


class TNAQueue(authorize.AccountsQueue):
    def __init__(self, accounts_path, api_token, **kwargs):
        super().__init__(accounts_path, **kwargs)
        self.api_token = api_token

    def first_check(self, account):
        url = f'https://api.tna-tickets.ru/api/v1/user/login-dls-token?' \
              f'access-token={self.api_token}'
        headers = {
            'authority': 'api.tna-tickets.ru',
            'method': 'POST',
            'path': f'/api/v1/user/login-dls-token?access-token={self.api_token}',
            'scheme': 'https',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'Content-Length': '575',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.ak-bars.ru',
            'Referer': 'https://www.ak-bars.ru/tickets/',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': self.user_agent
        }
        data = {'token': account.ak_token}
        r = account.post(url, headers=headers, data=data)
        if isinstance(r.json(), list):
            logger.info(r.json())
        acc_data = r.json()['result']
        account.data = acc_data

        url = f'https://api.tna-tickets.ru/api/v1/order?access-token' \
              f'={self.api_token}&user_token={acc_data["user_token"]}'
        headers = {
            'authority': 'api.tna-tickets.ru',
            'method': 'GET',
            'path': f'/api/v1/order?access-token={self.api_token}'
                    f'&user_token={acc_data["user_token"]}',
            'scheme': 'https',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.ak-bars.ru',
            'Referer': 'https://www.ak-bars.ru/tickets/orders',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': self.user_agent
        }
        r = account.get(url, headers=headers)

        to_del = {order['id']: int(order['seatquant'])
                  for order in r.json()['result']
                  if order['paystatusname'] == 'Неоплачено'}
        account.bought = {order['calendar_id']: int(order['seatquant'])
                          for order in r.json()['result']
                          if order['paystatusname'] != 'Неоплачено'}

        for order in to_del:
            url = f'https://api.tna-tickets.ru/api/v1/order/{order}/delete' \
                  f'?access-token={self.api_token}&user_token={acc_data["user_token"]}'
            headers = {
                'authority': 'api.tna-tickets.ru',
                'method': 'POST',
                'path': f'/api/v1/order/{order}/delete?access-token'
                        f'={self.api_token}&user_token={acc_data["user_token"]}',
                'scheme': 'https',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ru-RU,ru;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://www.ak-bars.ru',
                'Referer': 'https://www.ak-bars.ru/tickets/orders',
                'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': self.user_agent
            }
            r = account.post(url, data={'id': order}, headers=headers)
            print(green(f'Order {order} deleted on {account}'))
        return True

    def is_logined(self, account):
        url = 'https://api.ak-bars.ru/portal/auth/user'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'Authorization': f'Bearer {account.ak_token}',
            'Connection': 'keep-alive',
            'Host': 'api.ak-bars.ru',
            'Origin': 'https://www.ak-bars.ru',
            'Referer': 'https://www.ak-bars.ru/tickets',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': self.user_agent,
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        r = account.get(url, headers=headers)

        status = False
        if 'user' in r.json():
            if 'login' in r.json()['user']:
                if r.json()['user']['login'] == account.login:
                    status = True
                else:
                    raise RuntimeError(f'Путаница в аккаунтах! {account} - {r.json()["user"]}')

        return status

    def login(self, account):
        url = 'https://api.ak-bars.ru/portal/auth/login'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '48',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': 'api.ak-bars.ru',
            'Origin': 'https://auth.ak-bars.ru',
            'Referer': 'https://auth.ak-bars.ru',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': self.user_agent,
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        data = {
            'login': account.login,
            'password': account.password,
        }
        r = account.post(url, headers=headers, json=data)

        error = r.json().get('error')
        if error:
            if 'зафиксировано слишком много попыток' in r.text:
                print(yellow(r.text))
                account.change_identity()
                return self.login(account)
            if 'Неверный логин или пароль' in r.text:
                print(yellow(r.text))
                self.ban(account)
            else:
                raise RuntimeError(f'Неизвестная ошибка авторизации: {error}')

        account.ak_token = r.headers.get('AK-Token', '')
        if not account.ak_token:
            raise RuntimeError(f'В ответном headers отсутствует токен авторизации: {r.text}')


if __name__ == '__main__':
    api_token = '5f4dbf2e5629d8cc19e7d51874266678'
    accounts = TNAQueue('authorize_accounts.txt', api_token, reauthorize=True)
    accounts.start()
    while True:
        input()
        print(accounts.qsize())
        account = accounts.get()
        print(account.data)
        print(accounts.is_logined(account))
