url = 'https://tickets.cska-hockey.ru/'
headers = {
   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'pragma': 'no-cache',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'document',
   'sec-fetch-mode': 'navigate',
   'sec-fetch-site': 'none',
   'sec-fetch-user': '?1',
   'upgrade-insecure-requests': '1',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://cska-hockey.ru/shop_list_iframe.php'
headers = {
   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'iframe',
   'sec-fetch-mode': 'navigate',
   'sec-fetch-site': 'same-site',
   'upgrade-insecure-requests': '1',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://tickets.cska-hockey.ru/cart/count'
headers = {
   'accept': '*/*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': self.user_agent,
   'x-requested-with': 'XMLHttpRequest',
}
r = self.session.get(url, headers=headers)


url = 'https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru'
headers = {
   'accept': '*/*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': self.user_agent,
   'x-requested-with': 'XMLHttpRequest',
}
r = self.session.get(url, headers=headers)


url = 'https://cska-hockey.ru/ajax/share.php'
headers = {
   'accept': 'text/html, */*; q=0.01',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'content-length': '0',
   'origin': 'https://cska-hockey.ru',
   'pragma': 'no-cache',
   'referer': 'https://cska-hockey.ru/shop_list_iframe.php',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': self.user_agent,
   'x-requested-with': 'XMLHttpRequest',
}
r = self.session.post(url, headers=headers)


url = 'https://tickets.cska-hockey.ru/user/login'
headers = {
   'accept': 'application/json, text/javascript, */*; q=0.01',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'content-length': '268',
   'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
   'origin': 'https://tickets.cska-hockey.ru',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': self.user_agent,
   'x-csrf-token': 'zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw==',
   'x-requested-with': 'XMLHttpRequest',
}
data = {
   '_csrf-frontend': 'zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw%3D%3D',
   'login-form%5Blogin%5D': 'k1pi4i%40yandex.ru',
   'login-form%5Bpassword%5D': '',
   'login-form%5BreCaptcha%5D': '',
   'g-recaptcha-response': '',
   'login-form%5BrememberMe%5D': '0',
   'ajax': 'login-form',
}

# _csrf-frontend: zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw%3D%3D
# sources: [
# ]
# login-form%5Blogin%5D: k1pi4i%40yandex.ru
# sources: [
# ]
# login-form%5Bpassword%5D: 
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: response_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: url
#     repr: 
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: response_cookies
#     repr: PHPSESSID: fVbAV4n6lHnRLG1oDasGfj8Wk6bkzZkm
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: url
#     repr: 
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: request_cookies
#     repr: _ga: GA1.2.1567665585.1682244882
#     
# ]
# login-form%5BreCaptcha%5D: 
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: response_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: url
#     repr: 
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: response_cookies
#     repr: PHPSESSID: fVbAV4n6lHnRLG1oDasGfj8Wk6bkzZkm
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: url
#     repr: 
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: request_cookies
#     repr: _ga: GA1.2.1567665585.1682244882
#     
# ]
# g-recaptcha-response: 
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: response_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: url
#     repr: 
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: response_cookies
#     repr: PHPSESSID: fVbAV4n6lHnRLG1oDasGfj8Wk6bkzZkm
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: url
#     repr: 
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: request_cookies
#     repr: _ga: GA1.2.1567665585.1682244882
#     
# ]
# login-form%5BrememberMe%5D: 0
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: response_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: request_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: request_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: request_cookies
#     repr: _gid: GA1.2.1442128024.1682244882
#     
# ]
# ajax: login-form
# sources: [
# ]

r = self.session.post(url, headers=headers, data=data)


url = 'https://tickets.cska-hockey.ru/user/login'
headers = {
   'accept': 'application/json, text/javascript, */*; q=0.01',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'content-length': '268',
   'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
   'origin': 'https://tickets.cska-hockey.ru',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': self.user_agent,
   'x-csrf-token': 'zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw==',
   'x-requested-with': 'XMLHttpRequest',
}
data = {
   '_csrf-frontend': 'zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw%3D%3D',
   'login-form%5Blogin%5D': 'k1pi4i%40yandex.ru',
   'login-form%5Bpassword%5D': '',
   'login-form%5BreCaptcha%5D': '',
   'g-recaptcha-response': '',
   'login-form%5BrememberMe%5D': '0',
   'ajax': 'login-form',
}

# _csrf-frontend: zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw%3D%3D
# sources: [
# ]
# login-form%5Blogin%5D: k1pi4i%40yandex.ru
# sources: [
# ]
# login-form%5Bpassword%5D: 
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: response_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: url
#     repr: 
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: response_cookies
#     repr: PHPSESSID: fVbAV4n6lHnRLG1oDasGfj8Wk6bkzZkm
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: url
#     repr: 
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: request_cookies
#     repr: _ga: GA1.2.1567665585.1682244882
#     
# ]
# login-form%5BreCaptcha%5D: 
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: response_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: url
#     repr: 
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: response_cookies
#     repr: PHPSESSID: fVbAV4n6lHnRLG1oDasGfj8Wk6bkzZkm
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: url
#     repr: 
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: request_cookies
#     repr: _ga: GA1.2.1567665585.1682244882
#     
# ]
# g-recaptcha-response: 
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: response_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: url
#     repr: 
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: response_cookies
#     repr: PHPSESSID: fVbAV4n6lHnRLG1oDasGfj8Wk6bkzZkm
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: url
#     repr: 
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: request_cookies
#     repr: _ga: GA1.2.1567665585.1682244882
#     
# ]
# login-form%5BrememberMe%5D: 0
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: response_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: request_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: request_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: request_cookies
#     repr: _gid: GA1.2.1442128024.1682244882
#     
# ]
# ajax: login-form
# sources: [
# ]

r = self.session.post(url, headers=headers, data=data)


url = 'https://tickets.cska-hockey.ru/user/login'
headers = {
   'accept': 'application/json, text/javascript, */*; q=0.01',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'content-length': '276',
   'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
   'origin': 'https://tickets.cska-hockey.ru',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': self.user_agent,
   'x-csrf-token': 'zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw==',
   'x-requested-with': 'XMLHttpRequest',
}
data = {
   '_csrf-frontend': 'zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw%3D%3D',
   'login-form%5Blogin%5D': 'k1pi4i%40yandex.ru',
   'login-form%5Bpassword%5D': '4AwBNIPY',
   'login-form%5BreCaptcha%5D': '',
   'g-recaptcha-response': '',
   'login-form%5BrememberMe%5D': '0',
   'ajax': 'login-form',
}

# _csrf-frontend: zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw%3D%3D
# sources: [
# ]
# login-form%5Blogin%5D: k1pi4i%40yandex.ru
# sources: [
# ]
# login-form%5Bpassword%5D: 4AwBNIPY
# sources: [
# ]
# login-form%5BreCaptcha%5D: 
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: response_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: url
#     repr: 
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: response_cookies
#     repr: PHPSESSID: fVbAV4n6lHnRLG1oDasGfj8Wk6bkzZkm
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: url
#     repr: 
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: request_cookies
#     repr: _ga: GA1.2.1567665585.1682244882
#     
# ]
# g-recaptcha-response: 
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: response_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: url
#     repr: 
#     
#     url: [GET] https://cska-hockey.ru/shop_list_iframe.php
#     place: response_cookies
#     repr: PHPSESSID: fVbAV4n6lHnRLG1oDasGfj8Wk6bkzZkm
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: request_cookies
#     repr: city_id: 2
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: url
#     repr: 
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: request_cookies
#     repr: _ga: GA1.2.1567665585.1682244882
#     
# ]
# login-form%5BrememberMe%5D: 0
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: response_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: request_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: request_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: request_cookies
#     repr: _gid: GA1.2.1442128024.1682244882
#     
# ]
# ajax: login-form
# sources: [
# ]

r = self.session.post(url, headers=headers, data=data)


url = 'https://tickets.cska-hockey.ru/user/login'
headers = {
   'accept': 'application/json, text/javascript, */*; q=0.01',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'content-length': '1372',
   'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
   'origin': 'https://tickets.cska-hockey.ru',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': self.user_agent,
   'x-csrf-token': 'zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw==',
   'x-requested-with': 'XMLHttpRequest',
}
data = {
   '_csrf-frontend': 'zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw%3D%3D',
   'login-form%5Blogin%5D': 'k1pi4i%40yandex.ru',
   'login-form%5Bpassword%5D': '4AwBNIPY',
   'login-form%5BreCaptcha%5D': '03AKH6MRFctMU5L0ao7m3mV_zZn0H1wdWHRLYI51Ks0qE2V2DWd32RKxfbuUx2VGj4rPNAAHjQQ4yDKiyEQdgHRUqYpdzc2jPfRb33dcEQ3fmyk3weHOyjzGyVGPeV9UMf_OK_5SvEWyhpRa9fRBKLt_bviPYdvmLOA5zWpzSmNkrlRaWl_-tgXaY199okdXCs9SPH40UTji1j9igFuNPiM9hFsizAvBy4N_XsHzQYEYGRK56ufq-3QYlY4trO9hQXub9WTx1eoQXEeWw6R5l1zwh9_wsdx9RUQZlEESNG9u3Cx-I1Zl5uG_tmVETi_VYkhEq50U-qaRM0ozKKGKNS_30zoyDPZTXU_DzBTO_8i82EmFq38CMlwRb7L4l1WeZJGHsOVdLeu4JNGQUo3nlBQVrri9xK_-5smo1cnGPMckmOlptIlSYZ6OWCVjQ-_ResZsqfgfvZq564m1YPinNcyjCM33SKvZYUcUvokQfaewGUUTJA4rX7O9gvi_t07SoZuwm9anrRQzW9tUKsJ40oVnH1E4uOMOE68g',
   'g-recaptcha-response': '03AKH6MRFctMU5L0ao7m3mV_zZn0H1wdWHRLYI51Ks0qE2V2DWd32RKxfbuUx2VGj4rPNAAHjQQ4yDKiyEQdgHRUqYpdzc2jPfRb33dcEQ3fmyk3weHOyjzGyVGPeV9UMf_OK_5SvEWyhpRa9fRBKLt_bviPYdvmLOA5zWpzSmNkrlRaWl_-tgXaY199okdXCs9SPH40UTji1j9igFuNPiM9hFsizAvBy4N_XsHzQYEYGRK56ufq-3QYlY4trO9hQXub9WTx1eoQXEeWw6R5l1zwh9_wsdx9RUQZlEESNG9u3Cx-I1Zl5uG_tmVETi_VYkhEq50U-qaRM0ozKKGKNS_30zoyDPZTXU_DzBTO_8i82EmFq38CMlwRb7L4l1WeZJGHsOVdLeu4JNGQUo3nlBQVrri9xK_-5smo1cnGPMckmOlptIlSYZ6OWCVjQ-_ResZsqfgfvZq564m1YPinNcyjCM33SKvZYUcUvokQfaewGUUTJA4rX7O9gvi_t07SoZuwm9anrRQzW9tUKsJ40oVnH1E4uOMOE68g',
   'login-form%5BrememberMe%5D': '0',
   'ajax': 'login-form',
}

# _csrf-frontend: zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw%3D%3D
# sources: [
# ]
# login-form%5Blogin%5D: k1pi4i%40yandex.ru
# sources: [
# ]
# login-form%5Bpassword%5D: 4AwBNIPY
# sources: [
# ]
# login-form%5BreCaptcha%5D: 03AKH6MRFctMU5L0ao7m3mV_zZn0H1wdWHRLYI51Ks0qE2V2DWd32RKxfbuUx2VGj4rPNAAHjQQ4yDKiyEQdgHRUqYpdzc2jPfRb33dcEQ3fmyk3weHOyjzGyVGPeV9UMf_OK_5SvEWyhpRa9fRBKLt_bviPYdvmLOA5zWpzSmNkrlRaWl_-tgXaY199okdXCs9SPH40UTji1j9igFuNPiM9hFsizAvBy4N_XsHzQYEYGRK56ufq-3QYlY4trO9hQXub9WTx1eoQXEeWw6R5l1zwh9_wsdx9RUQZlEESNG9u3Cx-I1Zl5uG_tmVETi_VYkhEq50U-qaRM0ozKKGKNS_30zoyDPZTXU_DzBTO_8i82EmFq38CMlwRb7L4l1WeZJGHsOVdLeu4JNGQUo3nlBQVrri9xK_-5smo1cnGPMckmOlptIlSYZ6OWCVjQ-_ResZsqfgfvZq564m1YPinNcyjCM33SKvZYUcUvokQfaewGUUTJA4rX7O9gvi_t07SoZuwm9anrRQzW9tUKsJ40oVnH1E4uOMOE68g
# sources: [
# ]
# g-recaptcha-response: 03AKH6MRFctMU5L0ao7m3mV_zZn0H1wdWHRLYI51Ks0qE2V2DWd32RKxfbuUx2VGj4rPNAAHjQQ4yDKiyEQdgHRUqYpdzc2jPfRb33dcEQ3fmyk3weHOyjzGyVGPeV9UMf_OK_5SvEWyhpRa9fRBKLt_bviPYdvmLOA5zWpzSmNkrlRaWl_-tgXaY199okdXCs9SPH40UTji1j9igFuNPiM9hFsizAvBy4N_XsHzQYEYGRK56ufq-3QYlY4trO9hQXub9WTx1eoQXEeWw6R5l1zwh9_wsdx9RUQZlEESNG9u3Cx-I1Zl5uG_tmVETi_VYkhEq50U-qaRM0ozKKGKNS_30zoyDPZTXU_DzBTO_8i82EmFq38CMlwRb7L4l1WeZJGHsOVdLeu4JNGQUo3nlBQVrri9xK_-5smo1cnGPMckmOlptIlSYZ6OWCVjQ-_ResZsqfgfvZq564m1YPinNcyjCM33SKvZYUcUvokQfaewGUUTJA4rX7O9gvi_t07SoZuwm9anrRQzW9tUKsJ40oVnH1E4uOMOE68g
# sources: [
# ]
# login-form%5BrememberMe%5D: 0
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: response_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: request_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: request_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: request_cookies
#     repr: _gid: GA1.2.1442128024.1682244882
#     
# ]
# ajax: login-form
# sources: [
# ]

r = self.session.post(url, headers=headers, data=data)


url = 'https://tickets.cska-hockey.ru/user/login'
headers = {
   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'content-length': '1356',
   'content-type': 'application/x-www-form-urlencoded',
   'origin': 'https://tickets.cska-hockey.ru',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'document',
   'sec-fetch-mode': 'navigate',
   'sec-fetch-site': 'same-origin',
   'sec-fetch-user': '?1',
   'upgrade-insecure-requests': '1',
   'user-agent': self.user_agent,
}
data = {
   '_csrf-frontend': 'zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw%3D%3D',
   'login-form%5Blogin%5D': 'k1pi4i%40yandex.ru',
   'login-form%5Bpassword%5D': '4AwBNIPY',
   'login-form%5BreCaptcha%5D': '03AKH6MRFctMU5L0ao7m3mV_zZn0H1wdWHRLYI51Ks0qE2V2DWd32RKxfbuUx2VGj4rPNAAHjQQ4yDKiyEQdgHRUqYpdzc2jPfRb33dcEQ3fmyk3weHOyjzGyVGPeV9UMf_OK_5SvEWyhpRa9fRBKLt_bviPYdvmLOA5zWpzSmNkrlRaWl_-tgXaY199okdXCs9SPH40UTji1j9igFuNPiM9hFsizAvBy4N_XsHzQYEYGRK56ufq-3QYlY4trO9hQXub9WTx1eoQXEeWw6R5l1zwh9_wsdx9RUQZlEESNG9u3Cx-I1Zl5uG_tmVETi_VYkhEq50U-qaRM0ozKKGKNS_30zoyDPZTXU_DzBTO_8i82EmFq38CMlwRb7L4l1WeZJGHsOVdLeu4JNGQUo3nlBQVrri9xK_-5smo1cnGPMckmOlptIlSYZ6OWCVjQ-_ResZsqfgfvZq564m1YPinNcyjCM33SKvZYUcUvokQfaewGUUTJA4rX7O9gvi_t07SoZuwm9anrRQzW9tUKsJ40oVnH1E4uOMOE68g',
   'g-recaptcha-response': '03AKH6MRFctMU5L0ao7m3mV_zZn0H1wdWHRLYI51Ks0qE2V2DWd32RKxfbuUx2VGj4rPNAAHjQQ4yDKiyEQdgHRUqYpdzc2jPfRb33dcEQ3fmyk3weHOyjzGyVGPeV9UMf_OK_5SvEWyhpRa9fRBKLt_bviPYdvmLOA5zWpzSmNkrlRaWl_-tgXaY199okdXCs9SPH40UTji1j9igFuNPiM9hFsizAvBy4N_XsHzQYEYGRK56ufq-3QYlY4trO9hQXub9WTx1eoQXEeWw6R5l1zwh9_wsdx9RUQZlEESNG9u3Cx-I1Zl5uG_tmVETi_VYkhEq50U-qaRM0ozKKGKNS_30zoyDPZTXU_DzBTO_8i82EmFq38CMlwRb7L4l1WeZJGHsOVdLeu4JNGQUo3nlBQVrri9xK_-5smo1cnGPMckmOlptIlSYZ6OWCVjQ-_ResZsqfgfvZq564m1YPinNcyjCM33SKvZYUcUvokQfaewGUUTJA4rX7O9gvi_t07SoZuwm9anrRQzW9tUKsJ40oVnH1E4uOMOE68g',
   'login-form%5BrememberMe%5D': '0',
}

# _csrf-frontend: zlgUF_r7W-7Vu0JfPWdEiAMlbhKSRwLdvzz0BFz0KmirYVpelaoRmu2IBxlVPmndUXYIe-oXcL_6ZMVuMoxfKw%3D%3D
# sources: [
# ]
# login-form%5Blogin%5D: k1pi4i%40yandex.ru
# sources: [
# ]
# login-form%5Bpassword%5D: 4AwBNIPY
# sources: [
# ]
# login-form%5BreCaptcha%5D: 03AKH6MRFctMU5L0ao7m3mV_zZn0H1wdWHRLYI51Ks0qE2V2DWd32RKxfbuUx2VGj4rPNAAHjQQ4yDKiyEQdgHRUqYpdzc2jPfRb33dcEQ3fmyk3weHOyjzGyVGPeV9UMf_OK_5SvEWyhpRa9fRBKLt_bviPYdvmLOA5zWpzSmNkrlRaWl_-tgXaY199okdXCs9SPH40UTji1j9igFuNPiM9hFsizAvBy4N_XsHzQYEYGRK56ufq-3QYlY4trO9hQXub9WTx1eoQXEeWw6R5l1zwh9_wsdx9RUQZlEESNG9u3Cx-I1Zl5uG_tmVETi_VYkhEq50U-qaRM0ozKKGKNS_30zoyDPZTXU_DzBTO_8i82EmFq38CMlwRb7L4l1WeZJGHsOVdLeu4JNGQUo3nlBQVrri9xK_-5smo1cnGPMckmOlptIlSYZ6OWCVjQ-_ResZsqfgfvZq564m1YPinNcyjCM33SKvZYUcUvokQfaewGUUTJA4rX7O9gvi_t07SoZuwm9anrRQzW9tUKsJ40oVnH1E4uOMOE68g
# sources: [
# ]
# g-recaptcha-response: 03AKH6MRFctMU5L0ao7m3mV_zZn0H1wdWHRLYI51Ks0qE2V2DWd32RKxfbuUx2VGj4rPNAAHjQQ4yDKiyEQdgHRUqYpdzc2jPfRb33dcEQ3fmyk3weHOyjzGyVGPeV9UMf_OK_5SvEWyhpRa9fRBKLt_bviPYdvmLOA5zWpzSmNkrlRaWl_-tgXaY199okdXCs9SPH40UTji1j9igFuNPiM9hFsizAvBy4N_XsHzQYEYGRK56ufq-3QYlY4trO9hQXub9WTx1eoQXEeWw6R5l1zwh9_wsdx9RUQZlEESNG9u3Cx-I1Zl5uG_tmVETi_VYkhEq50U-qaRM0ozKKGKNS_30zoyDPZTXU_DzBTO_8i82EmFq38CMlwRb7L4l1WeZJGHsOVdLeu4JNGQUo3nlBQVrri9xK_-5smo1cnGPMckmOlptIlSYZ6OWCVjQ-_ResZsqfgfvZq564m1YPinNcyjCM33SKvZYUcUvokQfaewGUUTJA4rX7O9gvi_t07SoZuwm9anrRQzW9tUKsJ40oVnH1E4uOMOE68g
# sources: [
# ]
# login-form%5BrememberMe%5D: 0
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/
#     place: response_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [GET] https://tickets.cska-hockey.ru/cart/count
#     place: request_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [GET] https://tickets.cska-hockey.ru/language/get-all-dictionary?lang=ru
#     place: request_cookies
#     repr: session: 07tt5a56i2a1923kmm6cs111ol
#     
#     url: [POST] https://cska-hockey.ru/ajax/share.php
#     place: request_cookies
#     repr: _gid: GA1.2.1442128024.1682244882
#     
# ]

r = self.session.post(url, headers=headers, data=data)


url = 'https://tickets.cska-hockey.ru/'
headers = {
   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'document',
   'sec-fetch-mode': 'navigate',
   'sec-fetch-site': 'same-origin',
   'sec-fetch-user': '?1',
   'upgrade-insecure-requests': '1',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://cska-hockey.ru/shop_list_iframe.php'
headers = {
   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'iframe',
   'sec-fetch-mode': 'navigate',
   'sec-fetch-site': 'same-site',
   'upgrade-insecure-requests': '1',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://tickets.cska-hockey.ru/cart/count'
headers = {
   'accept': '*/*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': self.user_agent,
   'x-requested-with': 'XMLHttpRequest',
}
r = self.session.get(url, headers=headers)


url = 'https://cska-hockey.ru/ajax/share.php'
headers = {
   'accept': 'text/html, */*; q=0.01',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'content-length': '0',
   'origin': 'https://cska-hockey.ru',
   'pragma': 'no-cache',
   'referer': 'https://cska-hockey.ru/shop_list_iframe.php',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': self.user_agent,
   'x-requested-with': 'XMLHttpRequest',
}
r = self.session.post(url, headers=headers)


url = 'https://tickets.cska-hockey.ru/event/?id=1039'
headers = {
   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'document',
   'sec-fetch-mode': 'navigate',
   'sec-fetch-site': 'same-origin',
   'sec-fetch-user': '?1',
   'upgrade-insecure-requests': '1',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://tickets.cska-hockey.ru/cart/count'
headers = {
   'accept': '*/*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/event/?id=1039',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': self.user_agent,
   'x-requested-with': 'XMLHttpRequest',
}
r = self.session.get(url, headers=headers)


url = 'https://tickets.cska-hockey.ru/event/get-prices'
headers = {
   'accept': '*/*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9',
   'cache-control': 'no-cache',
   'content-length': '121',
   'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
   'origin': 'https://tickets.cska-hockey.ru',
   'pragma': 'no-cache',
   'referer': 'https://tickets.cska-hockey.ru/event/?id=1039',
   'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-origin',
   'user-agent': self.user_agent,
   'x-requested-with': 'XMLHttpRequest',
}
data = {
   'event_id': '1039',
   '_csrf-frontend': 'NbgTu7lGUR3w60kvzObRdGBNQfet7MjpfQVUtb-G9xJ07Ub_jQ04S5S6fhf6r5AQJHQFkcmm-54-fWfcju6APw%3D%3D',
}

# event_id: 1039
# sources: [
#     url: [GET] https://tickets.cska-hockey.ru/event/?id=1039
#     place: url
#     repr: 
#     
#     url: [GET] https://tickets.cska-hockey.ru/event/?id=1039
#     place: r_text
#     repr: ets.cska-chockey.ru/event/?id=1039"><meta property="og:image" c
#     
# ]
# _csrf-frontend: NbgTu7lGUR3w60kvzObRdGBNQfet7MjpfQVUtb-G9xJ07Ub_jQ04S5S6fhf6r5AQJHQFkcmm-54-fWfcju6APw%3D%3D
# sources: [
# ]

r = self.session.post(url, headers=headers, data=data)
