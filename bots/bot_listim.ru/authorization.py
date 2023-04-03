import os
import sys
import requests
from requests.utils import dict_from_cookiejar

s_path = os.path.dirname(os.path.abspath(__file__)).split('\\')[:-1]
sys.path.insert(0, '\\'.join(s_path) + '\\[MySources]')
import authorize
from vis import *
from cores import *

class ListimQueue(authorize.AccountsQueue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def first_check(self, account):
        try:
            account.xsrf_token
        except:
            account.xsrf_token = self.get_xsrf(account)
    
        url = 'https://listim.com/iframe/423/api/basket/info?lang=ru'
        headers = {
            'authority': 'listim.com',
            'method': 'POST',
            'path': get_path(url),
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '0',
            'origin': 'https://listim.com',
            'pragma': 'no-cache',
            'referer': 'https://listim.com/iframe/423/api',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-xsrf-token': account.xsrf_token
        }
        
        r = account.post(url, verify=False, headers=headers)
        
        if 'шибка 403' in r.text:
            error = "Ошибка 403"
            account.change_identity()
            account.xsrf_token = self.get_xsrf(account)
            print(yellow('First check retrying'))
            return self.first_check(account)
        
        if 'places' not in r.json():
            raise RuntimeError('Неверный ответ: ' + r.text[:100])
            
        cart_events = [place['id'] for place in r.json()['places']]
        
        url = 'https://listim.com/iframe/423/api/basket/unreserve_place?lang=ru'
        headers = {
            'authority': 'listim.com',
            'method': 'POST',
            'path': get_path(url),
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '23',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://listim.com',
            'pragma': 'no-cache',
            'referer': 'https://listim.com/iframe/423/api',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-xsrf-token': account.xsrf_token
        }
        
        for event_id in cart_events:
            form_data = {
                'event_place_id': event_id
            }
            
            r = account.post(url, verify=False, data=form_data, headers=headers)
            
        return True
    
    def is_logined(self, account):
        try:
            account.xsrf_token
        except:
            account.xsrf_token = self.get_xsrf(account)
        url = 'https://listim.com/iframe/423/api/auth/info?lang=ru'
        headers = {
            'authority': 'listim.com',
            'method': 'POST',
            'path': get_path(url),
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '0',
            'origin': 'https://listim.com',
            'pragma': 'no-cache',
            'referer': 'https://listim.com/iframe/423/api',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-xsrf-token': account.xsrf_token
        }
        
        r = account.post(url, verify=False, headers=headers)
        
        status = 0 if 'error' in r.text else 1
        return status
                
    def login(self, account, try_=1):
        tries = 100
        try:
            account.xsrf_token
        except:
            account.xsrf_token = self.get_xsrf(account)
        ### sitekey - https://listim.com/widget/partner/js/main.413239afd2e466138a24.js
        try:
            token, captcha_id = recaptcha_v3('6LcEuKgUAAAAANSADRhSE-hVsprpcSKjLWYabwHo', 'login',
                                 'https://listim.com/iframe/423/api/', min_score=0.6, mode=0, report=True)
        except: # ВОТ ТУТ НЕ НАДО
            if try_ < tries:
                return self.login(account, try_=try_+1)
            else:
                raise RuntimeError(f'Couldn\'t login in {try_} tries')
        url = 'https://listim.com/iframe/423/api/auth/login?lang=en-US'
        headers = {
            'authority': 'listim.com',
            'method': 'POST',
            'path': get_path(url),
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '521',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://listim.com',
            'pragma': 'no-cache',
            'referer': 'https://listim.com/iframe/423/api',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-xsrf-token': account.xsrf_token
        }
        
        form_data = {
            'email': account.login,
            'password': account.password,
            'token': token
        }
        
        r = account.post(url, data=form_data, verify=False, headers=headers)
        
        if ('error' in r.text) or ('шибка 403' in r.text):
            try:
                error = unicode_fix(r.json()['error']['text'])
            except:
                if 'шибка 403' in r.text:
                    error = "Ошибка 403"
                else:
                    error = r.text
                    
            if 'не совпад' in error:
                print(yellow(f'#{try_} {error}'))
                self.ban(account)
            elif 'подозрит' in error: # ТОКЕН НЕ СРАБОТАЛ ДЕЛАЕМ reportbad СНИЗУ
                recaptcha_v3_report(captcha_id, 0) # 0 - bad, 1 - good
                print(yellow(f'#{try_} {error}'))
                if try_ < tries:
                    self.login(account, try_=try_+1)
                else:
                    raise RuntimeError(f'Couldn\'t login in {try_} tries')
            elif "Ошибка 403" in error:
                print(yellow(f'#{try_} {error}'))
                account.change_identity()
                account.xsrf_token = self.get_xsrf(account)
                if try_ < tries:
                    self.login(account, try_=try_+1)
                else:
                    raise RuntimeError(f'Couldn\'t login in {try_} tries')
            else:
                raise RuntimeError(error)
        else: # ТОКЕН СРАБОТАЛ ДЕЛАЕМ reportgood
            recaptcha_v3_report(captcha_id, 1) # 0 - bad, 1 - good
            print(green(f'Success solving captcha on try({try_})'))
            self.mean_try_login.append(try_)
        
    def get_xsrf(self, account, try_=1):
        url = 'https://listim.com/iframe/423/api'
        headers = {
            'authority': 'listim.com',
            'method': 'GET',
            'path': get_path(url),
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
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
        r = account.get(url, verify=False, headers=headers)
        if 'XSRF-TOKEN' in account.session.cookies.get_dict():
            return account.session.cookies.get_dict()['XSRF-TOKEN']
        else:
            if try_ <= 4:
                account.change_identity()
                return self.get_xsrf(account, try_=try_+1)
            else:
                raise RuntimeError(f'no XSRF-TOKEN in {try_-1} tries')

                             
if __name__ == '__main__':
    accounts = ListimQueue('authorize_accounts.txt', mix=True)
    accounts.start()
    while True:
        input()
        print(accounts.qsize())