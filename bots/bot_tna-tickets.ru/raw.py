url = 'https://www.ak-bars.ru/tickets/13722'
headers = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'Cache-Control': 'no-cache',
   'Connection': 'keep-alive',
   'Host': 'www.ak-bars.ru',
   'Pragma': 'no-cache',
   'Referer': 'https://auth.ak-bars.ru/',
   'Sec-Fetch-Dest': 'document',
   'Sec-Fetch-Mode': 'navigate',
   'Sec-Fetch-Site': 'same-origin',
   'Sec-Fetch-User': '?1',
   'Upgrade-Insecure-Requests': '1',
   'User-Agent': self.user_agent,
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
}
r = self.session.get(url, headers=headers)


url = 'https://api.ak-bars.ru/portal/sponsors?club_id=1'
headers = {
   'Accept': 'application/json, text/plain, */*',
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'Cache-Control': 'no-cache',
   'Connection': 'keep-alive',
   'Host': 'api.ak-bars.ru',
   'Origin': 'https://www.ak-bars.ru',
   'Pragma': 'no-cache',
   'Referer': 'https://www.ak-bars.ru/tickets/13722',
   'Sec-Fetch-Dest': 'empty',
   'Sec-Fetch-Mode': 'cors',
   'Sec-Fetch-Site': 'same-site',
   'User-Agent': self.user_agent,
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/team?access-token=5f4dbf2e5629d8cc19e7d51874266678'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode='
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&booking_id=13722'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&sport=1'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://www.ak-bars.ru/site.webmanifest?v=2'
headers = {
   'Accept': '*/*',
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'Cache-Control': 'no-cache',
   'Connection': 'keep-alive',
   'Host': 'www.ak-bars.ru',
   'Pragma': 'no-cache',
   'Referer': 'https://www.ak-bars.ru/tickets/13722',
   'Sec-Fetch-Dest': 'manifest',
   'Sec-Fetch-Mode': 'cors',
   'Sec-Fetch-Site': 'same-origin',
   'User-Agent': self.user_agent,
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/booking/seat-reserve?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'content-length': '69',
   'content-type': 'application/x-www-form-urlencoded',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
data = {
   'seat_id': '696',
   'seat_zone': '100',
   'booking_id': '13722',
   'booking_ids': '',
   'category_id': '2',
}

# seat_id: 696
# sources: [
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr: d>\r\n<td class=\"seat\" id=\"696\"><span>7</span></td>\r\n<td
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr: ullname":"Общий","color":"16776960"},{"id":"54890","category_id
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr:
#
# ]
# seat_zone: 100
# sources: [
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: r_text
#     repr: e_id":"-99999","zonetype_id":"100","seattype_id":"-99999","seat
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: r_text
#     repr: category_id":"2","minprice":"1100.00","maxprice":"1200.00","dis
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr: :200,"result":"<table width=\"100%\" cellpadding=\"4\" name=\"С
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr: "zone_id":"71","zonetype_id":"100"}],"status":200,"count":1}
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr: ,"zone_id":"2","zonetype_id":"100","price":"3000.00","discount"
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr: "zone_id":"71","zonetype_id":"100"}],"status":200,"count":1}
#
# ]
# booking_id: 13722
# sources: [
#     url: [GET] https://www.ak-bars.ru/tickets/13722
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&booking_id=13722
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
# ]
# booking_ids:
# sources: [
#     url: [GET] https://www.ak-bars.ru/tickets/13722
#     place: url
#     repr:
#
#     url: [GET] https://www.ak-bars.ru/tickets/13722
#     place: request_cookies
#     repr: _ym_uid: 1679909268361930235
#
#     url: [GET] https://pixel.konnektu.ru/getUserId
#     place: url
#     repr:
#
#     url: [GET] https://pixel.konnektu.ru/getUserId
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: url
#     repr:
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: response_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [OPTIONS] https://pixel.konnektu.ru/event
#     place: url
#     repr:
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: url
#     repr:
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: response_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [OPTIONS] https://pixel.konnektu.ru/event
#     place: url
#     repr:
#
#     url: [GET] https://api-video.khl.ru/khl/scripts/khl_id.html
#     place: url
#     repr:
#
#     url: [GET] https://api-video.khl.ru/khl/scripts/khl_id.html
#     place: request_cookies
#     repr: khl_id: AAAAHGQhYZm9jbHHBH4EAg==
#
#     url: [POST] https://sentry.kazansoft.ru/api/7/envelope/?sentry_key=49588cd0871f4179854d47981811d239&sentry_version=7
#     place: url
#     repr:
#
#     url: [GET] https://api.ak-bars.ru/portal/sponsors?club_id=1
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/team?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/team?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: response_cookies
#     repr: _csrf: a56cb4994d85dd631a6396fcc4bf3ffd45d22e22ef4dc4b5753d932a4e2242a0a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22ybTsMtY6p-UK0IzoyUBsY2DDDRiYdmY9%22%3B%7D
#
#     url: [GET] https://www.khl.ru/nav/khl/index_ru.php
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: response_cookies
#     repr: _csrf: eaad4d59ab0514a1f778e156aa73ad0a9703532b33088489a877f39787cd9aeea%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22ug8_c5Hwl9GuOm27V7I8vh8qjkEQsjrP%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&booking_id=13722
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&booking_id=13722
#     place: response_cookies
#     repr: _csrf: 23449aaae3cf3fba2095c2d37eb6d913ff3f7afb1acf335e90f3b517dfb81678a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%227jfI_D-mC5wfxXTs_TdnJInMAX-lX7p1%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: response_cookies
#     repr: _csrf: 632bbf7aea8a6882884e95e06b73f9c1ce882d8f557326fa48f33ceee17161c9a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22YEPFXRDFbKmFE6UFqIX1G1gG809FbYdZ%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: r_text
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&sport=1
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&sport=1
#     place: response_cookies
#     repr: _csrf: 73ad03f0d2e6afe4fc58a9848be3e8192901ff41b606badcb0eb6555247e28baa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22d73Q_Wccd38t3yJ_ifq2CimsLmosLYxm%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: response_cookies
#     repr: _csrf: 25892206302e4d58a251e08b82de07a4d7e76f4ab1c934f46b7e12c6648df875a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22pOKVGtwXPCT2Jv6cH65bkBeDV7on-z-e%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: r_text
#     repr:
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: url
#     repr:
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: response_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [OPTIONS] https://pixel.konnektu.ru/event
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: response_cookies
#     repr: _csrf: 20400ce58713132142b203a7d84366556cadcb6612158e62bfad316493f4534ba%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22yUn-EQnE2yKCtkp3YCmNUNFp-hQZsHDh%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: response_cookies
#     repr: _csrf: 69477ab817adc157777c6e1f8ababe836efad22e8d905bd4582fc700b18533baa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22LjCbzhgwjHujp0qq-53tBRw-fHsFVDaW%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr:
#
#     url: [GET] https://www.ak-bars.ru/site.webmanifest?v=2
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: response_cookies
#     repr: _csrf: b1034a8f8a88db7a524a8860ff6c6d83a8658af5e208a8028d877176ac2698a2a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%224DnA-H0R57HPBBv1qqGBdkKc_-l8qt85%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: response_cookies
#     repr: _csrf: cbf4e610aeed55547a4729cbe6d85079de0c4374534746e330d1469f2070c2cfa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22e4pacd9FqLpY7S0ZNtCa0L_e07RJdc3K%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr:
#
# ]
# category_id: 2
# sources: [
#     url: [GET] https://www.ak-bars.ru/tickets/13722
#     place: url
#     repr:
#
#     url: [GET] https://www.ak-bars.ru/tickets/13722
#     place: request_cookies
#     repr: _ym_uid: 1679909268361930235
#
#     url: [GET] https://pixel.konnektu.ru/getUserId
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: response_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: response_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [GET] https://api-video.khl.ru/khl/scripts/khl_id.html
#     place: request_cookies
#     repr: _ym_uid: 1679918225763191306
#
#     url: [POST] https://sentry.kazansoft.ru/api/7/envelope/?sentry_key=49588cd0871f4179854d47981811d239&sentry_version=7
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/team?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/team?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: response_cookies
#     repr: _csrf: a56cb4994d85dd631a6396fcc4bf3ffd45d22e22ef4dc4b5753d932a4e2242a0a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22ybTsMtY6p-UK0IzoyUBsY2DDDRiYdmY9%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: response_cookies
#     repr: _csrf: eaad4d59ab0514a1f778e156aa73ad0a9703532b33088489a877f39787cd9aeea%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22ug8_c5Hwl9GuOm27V7I8vh8qjkEQsjrP%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&booking_id=13722
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&booking_id=13722
#     place: response_cookies
#     repr: _csrf: 23449aaae3cf3fba2095c2d37eb6d913ff3f7afb1acf335e90f3b517dfb81678a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%227jfI_D-mC5wfxXTs_TdnJInMAX-lX7p1%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: response_cookies
#     repr: _csrf: 632bbf7aea8a6882884e95e06b73f9c1ce882d8f557326fa48f33ceee17161c9a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22YEPFXRDFbKmFE6UFqIX1G1gG809FbYdZ%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: r_text
#     repr: _id":"-99999","seatclass_id":"20","thumb":"https://api.tna-ti
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&sport=1
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&sport=1
#     place: response_cookies
#     repr: _csrf: 73ad03f0d2e6afe4fc58a9848be3e8192901ff41b606badcb0eb6555247e28baa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22d73Q_Wccd38t3yJ_ifq2CimsLmosLYxm%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: response_cookies
#     repr: _csrf: 25892206302e4d58a251e08b82de07a4d7e76f4ab1c934f46b7e12c6648df875a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22pOKVGtwXPCT2Jv6cH65bkBeDV7on-z-e%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: r_text
#     repr:
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: response_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: response_cookies
#     repr: _csrf: 20400ce58713132142b203a7d84366556cadcb6612158e62bfad316493f4534ba%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22yUn-EQnE2yKCtkp3YCmNUNFp-hQZsHDh%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: response_cookies
#     repr: _csrf: 69477ab817adc157777c6e1f8ababe836efad22e8d905bd4582fc700b18533baa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22LjCbzhgwjHujp0qq-53tBRw-fHsFVDaW%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr: seat_id":"696","name":"Сектор 2A Ряд 16 Место 7","quant":"1",
#
#     url: [GET] https://www.ak-bars.ru/site.webmanifest?v=2
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: response_cookies
#     repr: _csrf: b1034a8f8a88db7a524a8860ff6c6d83a8658af5e208a8028d877176ac2698a2a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%224DnA-H0R57HPBBv1qqGBdkKc_-l8qt85%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr: [{"id":"54910","category_id":"2","zone_id":"2","zonetype_id":
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: response_cookies
#     repr: _csrf: cbf4e610aeed55547a4729cbe6d85079de0c4374534746e330d1469f2070c2cfa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22e4pacd9FqLpY7S0ZNtCa0L_e07RJdc3K%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr: seat_id":"696","name":"Сектор 2A Ряд 16 Место 7","quant":"1",
#
# ]

r = self.session.post(url, headers=headers, data=data)


url = 'https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode='
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/order/create?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'content-length': '10',
   'content-type': 'application/x-www-form-urlencoded',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
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

# promocode:
# sources: [
#     url: [GET] https://www.ak-bars.ru/tickets/13722
#     place: url
#     repr:
#
#     url: [GET] https://www.ak-bars.ru/tickets/13722
#     place: request_cookies
#     repr: _ym_uid: 1679909268361930235
#
#     url: [GET] https://pixel.konnektu.ru/getUserId
#     place: url
#     repr:
#
#     url: [GET] https://pixel.konnektu.ru/getUserId
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: url
#     repr:
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: response_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [OPTIONS] https://pixel.konnektu.ru/event
#     place: url
#     repr:
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: url
#     repr:
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: response_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [OPTIONS] https://pixel.konnektu.ru/event
#     place: url
#     repr:
#
#     url: [GET] https://api-video.khl.ru/khl/scripts/khl_id.html
#     place: url
#     repr:
#
#     url: [GET] https://api-video.khl.ru/khl/scripts/khl_id.html
#     place: request_cookies
#     repr: khl_id: AAAAHGQhYZm9jbHHBH4EAg==
#
#     url: [POST] https://sentry.kazansoft.ru/api/7/envelope/?sentry_key=49588cd0871f4179854d47981811d239&sentry_version=7
#     place: url
#     repr:
#
#     url: [GET] https://api.ak-bars.ru/portal/sponsors?club_id=1
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/team?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/team?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: response_cookies
#     repr: _csrf: a56cb4994d85dd631a6396fcc4bf3ffd45d22e22ef4dc4b5753d932a4e2242a0a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22ybTsMtY6p-UK0IzoyUBsY2DDDRiYdmY9%22%3B%7D
#
#     url: [GET] https://www.khl.ru/nav/khl/index_ru.php
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: response_cookies
#     repr: _csrf: eaad4d59ab0514a1f778e156aa73ad0a9703532b33088489a877f39787cd9aeea%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22ug8_c5Hwl9GuOm27V7I8vh8qjkEQsjrP%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&booking_id=13722
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&booking_id=13722
#     place: response_cookies
#     repr: _csrf: 23449aaae3cf3fba2095c2d37eb6d913ff3f7afb1acf335e90f3b517dfb81678a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%227jfI_D-mC5wfxXTs_TdnJInMAX-lX7p1%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: response_cookies
#     repr: _csrf: 632bbf7aea8a6882884e95e06b73f9c1ce882d8f557326fa48f33ceee17161c9a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22YEPFXRDFbKmFE6UFqIX1G1gG809FbYdZ%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: r_text
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&sport=1
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&sport=1
#     place: response_cookies
#     repr: _csrf: 73ad03f0d2e6afe4fc58a9848be3e8192901ff41b606badcb0eb6555247e28baa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22d73Q_Wccd38t3yJ_ifq2CimsLmosLYxm%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: response_cookies
#     repr: _csrf: 25892206302e4d58a251e08b82de07a4d7e76f4ab1c934f46b7e12c6648df875a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22pOKVGtwXPCT2Jv6cH65bkBeDV7on-z-e%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: r_text
#     repr:
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: url
#     repr:
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: response_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [OPTIONS] https://pixel.konnektu.ru/event
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: response_cookies
#     repr: _csrf: 20400ce58713132142b203a7d84366556cadcb6612158e62bfad316493f4534ba%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22yUn-EQnE2yKCtkp3YCmNUNFp-hQZsHDh%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: response_cookies
#     repr: _csrf: 69477ab817adc157777c6e1f8ababe836efad22e8d905bd4582fc700b18533baa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22LjCbzhgwjHujp0qq-53tBRw-fHsFVDaW%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr:
#
#     url: [GET] https://www.ak-bars.ru/site.webmanifest?v=2
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: response_cookies
#     repr: _csrf: b1034a8f8a88db7a524a8860ff6c6d83a8658af5e208a8028d877176ac2698a2a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%224DnA-H0R57HPBBv1qqGBdkKc_-l8qt85%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: response_cookies
#     repr: _csrf: cbf4e610aeed55547a4729cbe6d85079de0c4374534746e330d1469f2070c2cfa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22e4pacd9FqLpY7S0ZNtCa0L_e07RJdc3K%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr:
#
#     url: [POST] https://api.tna-tickets.ru/api/v1/booking/seat-reserve?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
#     url: [POST] https://api.tna-tickets.ru/api/v1/booking/seat-reserve?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: response_cookies
#     repr: advanced-api: 7t03700ugcn7dkc4j576asgap3
#
#     url: [POST] https://api.tna-tickets.ru/api/v1/booking/seat-reserve?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: response_cookies
#     repr: _csrf: b7faa7c30c3575f09ecc1cb8f4ed97c13773ee976dbca8b74edba9f5bd46368ca%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22o2su_O8oXMnODfrSCQHfUyEyMTW7kIOl%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: r_text
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: response_cookies
#     repr: _csrf: cfdd28b0f4efda4bf1a75d3e3e654d0798f13ef74c9502c715c4946b72eba089a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22bdyhpIZvs2rwj-BfmJS_SF07GY0bZMU0%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr: lt":[],"status":200,"cou
#
# ]

r = self.session.post(url, headers=headers, data=data)


url = 'https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/13722',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://sentry.kazansoft.ru/api/7/envelope/?sentry_key=49588cd0871f4179854d47981811d239&sentry_version=7'
headers = {
   'Accept': '*/*',
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'Cache-Control': 'no-cache',
   'Connection': 'keep-alive',
   'Content-Length': '477',
   'Content-Type': 'text/plain;charset=UTF-8',
   'Host': 'sentry.kazansoft.ru',
   'Origin': 'https://www.ak-bars.ru',
   'Pragma': 'no-cache',
   'Referer': 'https://www.ak-bars.ru/',
   'Sec-Fetch-Dest': 'empty',
   'Sec-Fetch-Mode': 'cors',
   'Sec-Fetch-Site': 'cross-site',
   'User-Agent': self.user_agent,
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
}
r = self.session.post(url, headers=headers)


url = 'https://sentry.kazansoft.ru/api/7/envelope/?sentry_key=49588cd0871f4179854d47981811d239&sentry_version=7'
headers = {
   'Accept': '*/*',
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'Cache-Control': 'no-cache',
   'Connection': 'keep-alive',
   'Content-Length': '472',
   'Content-Type': 'text/plain;charset=UTF-8',
   'Host': 'sentry.kazansoft.ru',
   'Origin': 'https://www.ak-bars.ru',
   'Pragma': 'no-cache',
   'Referer': 'https://www.ak-bars.ru/',
   'Sec-Fetch-Dest': 'empty',
   'Sec-Fetch-Mode': 'cors',
   'Sec-Fetch-Site': 'cross-site',
   'User-Agent': self.user_agent,
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
}
r = self.session.post(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/order?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/orders/636509',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/order/636509?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/orders/636509',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/dls/balance?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d'
headers = {
   'accept': 'application/json, text/plain, */*',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'origin': 'https://www.ak-bars.ru',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/orders/636509',
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'cross-site',
   'user-agent': self.user_agent,
}
r = self.session.get(url, headers=headers)


url = 'https://api.tna-tickets.ru/api/v1/zenit/payment?orderHash=%D0%B03%0C%B3%BBF%10%C3%05%C4w%AE%3B%E8%A3aa5f9ef6e8ac4b251310b56a55c46740d462e8fcd4dde339e5471e19cf4eb2e4%B9%DE%E6M%8Cr%0CUW%9C%7CK%1C%3A%DF4%B23%AE%A2%90%A59%C0f%84%25%E0cm%96%B6&bonuses=0&backUrl=https://www.ak-bars.ru/tickets/orders/636509'
headers = {
   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'cache-control': 'no-cache',
   'pragma': 'no-cache',
   'referer': 'https://www.ak-bars.ru/tickets/orders/636509',
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
r = self.session.get(url, headers=headers)


url = 'https://3ds.zenit.ru/cgi-bin/cgi_link'
headers = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language': 'en-MY,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,vi;q=0.5',
   'Cache-Control': 'no-cache',
   'Connection': 'keep-alive',
   'Content-Length': '906',
   'Content-Type': 'application/x-www-form-urlencoded',
   'Host': '3ds.zenit.ru',
   'Origin': 'https://api.tna-tickets.ru',
   'Pragma': 'no-cache',
   'Referer': 'https://api.tna-tickets.ru/',
   'Sec-Fetch-Dest': 'document',
   'Sec-Fetch-Mode': 'navigate',
   'Sec-Fetch-Site': 'cross-site',
   'Upgrade-Insecure-Requests': '1',
   'User-Agent': self.user_agent,
   'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
}
data = {
   'TRTYPE': '1',
   'AMOUNT': '2050',
   'TERMINAL': '88000715',
   'CURRENCY': 'RUB',
   'ORDER': '000636509',
   'NONCE': '3ecd7c109763e9ba62ade23ad4b2872c',
   'BACKREF': 'https%3A%2F%2Fwww.ak-bars.ru%2Ftickets%2Forders%2F636509',
   'DESC': 'Order%3A000636509',
   'NOTIFY_URL': 'https%3A%2F%2Fapi.tna-tickets.ru%2Fapi%2Fv1%2Fzenit%2Fcheck',
   'P_SIGN': 'e0cab35802092034234a0cbd13fb4ab80feb86291f8972caac2e9fadab630b87',
   'COUNTRY': '643',
   'TIMESTAMP': '20230403122838',
   'MERCHANT': '88000715',
   'MERCH_INN': '1657230250',
   'MERCH_FISCAL_KEY': '3010094',
   'FISCAL_RECEIPT': 'eyJ0eXBlIjoxLCJwb3NpdGlvbnMiOlt7InF1YW50aXR5IjoiMSIsInByaWNlIjoyMDUwLCJ0YXgiOjYsInRleHQiOiLQpNC40L3QsNC7INCa0L7QvdGE0LXRgNC10L3RhtC40Lgg0JLQntCh0KLQntCaICDQpdCaIMKr0JDQuiDQkdCw0YDRgcK7IC0g0KXQmiDCq9CQ0LLQsNC90LPQsNGA0LTCuyAiLCJwYXltZW50U3ViamVjdFR5cGUiOjQsInBheW1lbnRNZXRob2RUeXBlIjoxfV0sImNoZWNrQ2xvc2UiOnsicGF5bWVudHMiOlt7InR5cGUiOjIsImFtb3VudCI6MjA1MH1dLCJ0YXhhdGlvblN5c3RlbSI6MH0sImN1c3RvbWVyQ29udGFjdCI6IkJhcmFuY2hpa0lnYW1rdWxpQG1haWwucnUifQ%3D%3D',
}

# TRTYPE: 1
# sources: [
#     url: [GET] https://www.ak-bars.ru/tickets/13722
#     place: url
#     repr:
#
#     url: [GET] https://www.ak-bars.ru/tickets/13722
#     place: request_cookies
#     repr: _ym_uid: 1679909268361930235
#
#     url: [GET] https://pixel.konnektu.ru/getUserId
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: response_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: response_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [GET] https://api-video.khl.ru/khl/scripts/khl_id.html
#     place: request_cookies
#     repr: _ym_uid: 1679918225763191306
#
#     url: [POST] https://sentry.kazansoft.ru/api/7/envelope/?sentry_key=49588cd0871f4179854d47981811d239&sentry_version=7
#     place: url
#     repr:
#
#     url: [GET] https://api.ak-bars.ru/portal/sponsors?club_id=1
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/team?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/team?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: response_cookies
#     repr: _csrf: a56cb4994d85dd631a6396fcc4bf3ffd45d22e22ef4dc4b5753d932a4e2242a0a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22ybTsMtY6p-UK0IzoyUBsY2DDDRiYdmY9%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: response_cookies
#     repr: _csrf: eaad4d59ab0514a1f778e156aa73ad0a9703532b33088489a877f39787cd9aeea%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22ug8_c5Hwl9GuOm27V7I8vh8qjkEQsjrP%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&booking_id=13722
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&booking_id=13722
#     place: response_cookies
#     repr: _csrf: 23449aaae3cf3fba2095c2d37eb6d913ff3f7afb1acf335e90f3b517dfb81678a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%227jfI_D-mC5wfxXTs_TdnJInMAX-lX7p1%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: response_cookies
#     repr: _csrf: 632bbf7aea8a6882884e95e06b73f9c1ce882d8f557326fa48f33ceee17161c9a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22YEPFXRDFbKmFE6UFqIX1G1gG809FbYdZ%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: r_text
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&sport=1
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/game?access-token=5f4dbf2e5629d8cc19e7d51874266678&sport=1
#     place: response_cookies
#     repr: _csrf: 73ad03f0d2e6afe4fc58a9848be3e8192901ff41b606badcb0eb6555247e28baa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22d73Q_Wccd38t3yJ_ifq2CimsLmosLYxm%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: response_cookies
#     repr: _csrf: 25892206302e4d58a251e08b82de07a4d7e76f4ab1c934f46b7e12c6648df875a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22pOKVGtwXPCT2Jv6cH65bkBeDV7on-z-e%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sectors-price?access-token=5f4dbf2e5629d8cc19e7d51874266678
#     place: r_text
#     repr:
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: request_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [POST] https://pixel.konnektu.ru/event
#     place: response_cookies
#     repr: knk_uid: cdd26842-420c-41c9-9688-18633e03dc22
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: response_cookies
#     repr: _csrf: 20400ce58713132142b203a7d84366556cadcb6612158e62bfad316493f4534ba%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22yUn-EQnE2yKCtkp3YCmNUNFp-hQZsHDh%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/sector-html?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr: :200,"result":"<table width=\"100%\" cellpadding=\"4\" name=\
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: response_cookies
#     repr: _csrf: 69477ab817adc157777c6e1f8ababe836efad22e8d905bd4582fc700b18533baa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22LjCbzhgwjHujp0qq-53tBRw-fHsFVDaW%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr: ":"696","name":"Сектор 2A Ряд 16 Место 7","quant":"1","color"
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: response_cookies
#     repr: _csrf: b1034a8f8a88db7a524a8860ff6c6d83a8658af5e208a8028d877176ac2698a2a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%224DnA-H0R57HPBBv1qqGBdkKc_-l8qt85%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: response_cookies
#     repr: _csrf: cbf4e610aeed55547a4729cbe6d85079de0c4374534746e330d1469f2070c2cfa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22e4pacd9FqLpY7S0ZNtCa0L_e07RJdc3K%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr: ":"696","name":"Сектор 2A Ряд 16 Место 7","quant":"1","color"
#
#     url: [POST] https://api.tna-tickets.ru/api/v1/booking/seat-reserve?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
#     url: [POST] https://api.tna-tickets.ru/api/v1/booking/seat-reserve?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr: 200,"result":[{"calendar_id":"13722","seat_id":"696","zone_id
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: response_cookies
#     repr: _csrf: b7faa7c30c3575f09ecc1cb8f4ed97c13773ee976dbca8b74edba9f5bd46368ca%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22o2su_O8oXMnODfrSCQHfUyEyMTW7kIOl%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: r_text
#     repr: lt":{"items":[{"calendar_id":"13722","person_id":"182673","se
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: response_cookies
#     repr: _csrf: cfdd28b0f4efda4bf1a75d3e3e654d0798f13ef74c9502c715c4946b72eba089a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22bdyhpIZvs2rwj-BfmJS_SF07GY0bZMU0%22%3B%7D
#
#     url: [POST] https://api.tna-tickets.ru/api/v1/order/create?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
#     url: [POST] https://api.tna-tickets.ru/api/v1/order/create?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: response_cookies
#     repr: _csrf: 279580145abf948e0199ae9e8b9682571e19f67f1a9c88ff14433cc151173481a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22dU0Myh433Yzwfbmg4uTI6Mm9z9qJNSAp%22%3B%7D
#
#     url: [POST] https://api.tna-tickets.ru/api/v1/order/create?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr: 36509","locktime":"03.04.2023 16:27","payment_link":"https://
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: response_cookies
#     repr: _csrf: 43bb7e40e505db5c234d1ef8a156dc362b968b4cecd9062280d648ea739ea3d4a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22sOTGo7P-M93xQW2FrWMydQM_ZINc3cj_%22%3B%7D
#
#     url: [POST] https://sentry.kazansoft.ru/api/7/envelope/?sentry_key=49588cd0871f4179854d47981811d239&sentry_version=7
#     place: url
#     repr:
#
#     url: [POST] https://sentry.kazansoft.ru/api/7/envelope/?sentry_key=49588cd0871f4179854d47981811d239&sentry_version=7
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/order?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/order?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: response_cookies
#     repr: _csrf: 7d2a040132a647cf446dc5cdb8620636bcdc4ad4db009a92995052328e1ac5d4a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22DhOgJerKd7vbAAEzcZD6A2m_U8J6EzQh%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/order?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr: atus_id":"20","paystatus_id":"10","paymean_id":"-40","company
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/order/636509?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/order/636509?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: response_cookies
#     repr: _csrf: 5c3e0c53053cbb994cb8fccedc50b7a9a79e1f79fbf4ca366efd05bd568e2279a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22MK-78sg3k-p7I-xoZbbSD1CrvdmnjQcU%22%3B%7D
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/order/636509?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr: r_id":"636509","calendar_id":"13722","calendarname":"Финал Ко
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/dls/balance?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: url
#     repr:
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/dls/balance?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr: ce":100}}
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/zenit/payment?orderHash=%D0%B03%0C%B3%BBF%10%C3%05%C4w%AE%3B%E8%A3aa5f9ef6e8ac4b251310b56a55c46740d462e8fcd4dde339e5471e19cf4eb2e4%B9%DE%E6M%8Cr%0CUW%9C%7CK%1C%3A%DF4%B23%AE%A2%90%A59%C0f%84%25%E0cm%96%B6&bonuses=0&backUrl=https://www.ak-bars.ru/tickets/orders/636509
#     place: url
#     repr:
#
# ]
# AMOUNT: 2050
# sources: [
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/13722/seats-price?access-token=5f4dbf2e5629d8cc19e7d51874266678&sector_id=394
#     place: r_text
#     repr: ,"zonetype_id":"100","price":"2050.00","discount":"0.00","zonena
#
#     url: [POST] https://api.tna-tickets.ru/api/v1/booking/seat-reserve?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr: 1","category_id":"2","price":"2050.00","quant":"1","pricemargin"
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/booking/cart?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d&promocode=
#     place: r_text
#     repr: :"Четвертая (центр)","price":"2050.00","quant":"1","pricemargin"
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/order?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr: alendartime":"19:30","price":"2050.00","paymentprice":"0.00","di
#
#     url: [GET] https://api.tna-tickets.ru/api/v1/order/636509?access-token=5f4dbf2e5629d8cc19e7d51874266678&user_token=368089bd40c2bb6c1f5113d9f1763f3d
#     place: r_text
#     repr: oryfullname":"Общий","price":"2050.00","quant":"1","printimage_i
#
# ]
# TERMINAL: 88000715
# sources: [
# ]
# CURRENCY: RUB
# sources: [
# ]
# ORDER: 000636509
# sources: [
# ]
# NONCE: 3ecd7c109763e9ba62ade23ad4b2872c
# sources: [
# ]
# BACKREF: https%3A%2F%2Fwww.ak-bars.ru%2Ftickets%2Forders%2F636509
# sources: [
# ]
# DESC: Order%3A000636509
# sources: [
# ]
# NOTIFY_URL: https%3A%2F%2Fapi.tna-tickets.ru%2Fapi%2Fv1%2Fzenit%2Fcheck
# sources: [
# ]
# P_SIGN: e0cab35802092034234a0cbd13fb4ab80feb86291f8972caac2e9fadab630b87
# sources: [
# ]
# COUNTRY: 643
# sources: [
# ]
# TIMESTAMP: 20230403122838
# sources: [
# ]
# MERCHANT: 88000715
# sources: [
# ]
# MERCH_INN: 1657230250
# sources: [
# ]
# MERCH_FISCAL_KEY: 3010094
# sources: [
# ]
# FISCAL_RECEIPT: eyJ0eXBlIjoxLCJwb3NpdGlvbnMiOlt7InF1YW50aXR5IjoiMSIsInByaWNlIjoyMDUwLCJ0YXgiOjYsInRleHQiOiLQpNC40L3QsNC7INCa0L7QvdGE0LXRgNC10L3RhtC40Lgg0JLQntCh0KLQntCaICDQpdCaIMKr0JDQuiDQkdCw0YDRgcK7IC0g0KXQmiDCq9CQ0LLQsNC90LPQsNGA0LTCuyAiLCJwYXltZW50U3ViamVjdFR5cGUiOjQsInBheW1lbnRNZXRob2RUeXBlIjoxfV0sImNoZWNrQ2xvc2UiOnsicGF5bWVudHMiOlt7InR5cGUiOjIsImFtb3VudCI6MjA1MH1dLCJ0YXhhdGlvblN5c3RlbSI6MH0sImN1c3RvbWVyQ29udGFjdCI6IkJhcmFuY2hpa0lnYW1rdWxpQG1haWwucnUifQ%3D%3D
# sources: [
# ]

r = self.session.post(url, headers=headers, data=data)
