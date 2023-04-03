import requests
from requests.utils import dict_from_cookiejar

from cores_src import authorize
from cores_src.vis import *
from cores_src.cores import *


class TNAQueue(authorize.AccountsQueue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ak_token = ''

    def first_check(self, account):
        # пока неизвестно как удалять билеты из корзины поэтому закоменчено
        return True

    def is_logined(self, account):
        url = 'https://api.ak-bars.ru/portal/auth/user'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'Authorization': f'Bearer {self.ak_token}',
            'Connection': 'keep-alive',
            'Host': 'api.ak-bars.ru',
            'Origin': 'https://www.ak-bars.ru',
            'Referer': 'https://www.ak-bars.ru/tickets/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': self.user_agent,
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        r = self.session.get(url, headers=headers)

        status = False
        if 'user' in r.json():
            if 'login' in r.json()['user']:
                if r.json()['user']['login'] == account.login:
                    status = True

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
            'Referer': 'https://auth.ak-bars.ru/',
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

        r = self.session.post(url, headers=headers, json=data)

        error = r.json().get('error')
        if error:
            if 'Неверный логин или пароль' in r.text:
                print(yellow(f'{r.text}'))
                self.ban(account)
                return False
            else:
                raise RuntimeError(f'Неизвестная ошибка авторизации: {error}')

        self.ak_token = r.headers.get('AK-Token', '')
        if not self.ak_token:
            raise RuntimeError(f'В ответном headers отсутствует токен авторизации: {r.text}')


if __name__ == '__main__':
    accounts = TNAQueue('authorize_accounts.txt')
    accounts.start()
    while True:
        input()
        print(accounts.qsize())
