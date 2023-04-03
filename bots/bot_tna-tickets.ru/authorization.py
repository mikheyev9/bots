import requests
from requests.utils import dict_from_cookiejar

from cores_src import authorize
from cores_src.vis import *
from cores_src.cores import *


class CSKAHQueue(authorize.AccountsQueue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def first_check(self, account):
        # пока неизвестно как удалять билеты из корзины поэтому закоменчено
        return True
    
    def is_logined(self, account):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'connection': 'keep-alive',
            'host': 'tickets.cska-hockey.ru',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }
        
        url = 'https://tickets.cska-hockey.ru/'
        r = account.get(url, headers=headers)
        
        status = True if '>выйти</a>' in r.text else False
        return status
                
    def login(self, account):
        headers = {
            'authority': 'tickets.cska-hockey.ru',
            'method': 'GET',
            'path': '/cart/count',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://tickets.cska-hockey.ru/user/login',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-requested-with': 'XMLHttpRequest'
        }
        
        url = 'https://tickets.cska-hockey.ru/user/login'
        r = account.get(url, headers=headers)
        # while 'queue.infomatika' in r.url:
        #    queue_site = double_split(r.text, '<span class="d-block">', '</span>')
        #    print(f'Очередь при входе в аккаунт, номер в очереди - {queue_site}')
        #    time.sleep(10)
        #    r = account.get(url, headers=headers)
        #    lprint(r.text)
        #print('Прошел')
        
        x_csrf_token = double_split(r.text, 'name="csrf-token" content="', '"')
        _csrf_frontend = double_split(r.text, 'name="_csrf-frontend" value="', '"')
        try:
            captcha_sitekey = double_split(r.text, 'ecaptcha" data-sitekey="', '"')
        except Exception as err:
            screen_r(r.text)
            raise RuntimeError('NO SITEKEY (auth): ' + str(err))
            
        
        login_url = 'https://tickets.cska-hockey.ru/user/login'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6',
            'cache-control': 'no-cache',
            'content-length': '1272',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://tickets.cska-hockey.ru',
            'pragma': 'no-cache',
            'referer': 'https://tickets.cska-hockey.ru',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }

        solved = BotCore.non_selenium_recaptcha(captcha_sitekey, url, print_logs=False)
            
        params = [
            ('_csrf-frontend', _csrf_frontend),
            ('login-form[login]', account.login),
            ('login-form[password]', account.password),
            ('login-form[reCaptcha]', solved),
            ('g-recaptcha-response', solved),
            ('login-form[rememberMe]', 0),
            ('login-form[rememberMe]', 0)
        ]
        r = account.post(login_url, data=params, headers=headers)
        
        if r.url != 'https://tickets.cska-hockey.ru':
            if 'Неверный E-mail или пароль' in r.text:
                self.ban(account)
                raise RuntimeError('Неправильный логин или пароль')
            else:
                raise RuntimeError(f'Другая ошибка во время логина: {r.text}')
    
    
if __name__ == '__main__':
    accounts = CSKAHQueue('authorize_accounts.txt')
    accounts.start()
    while True:
        input()
        print(accounts.qsize())