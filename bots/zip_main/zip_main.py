from cores_src.cores import *
from cores_src.vis import *

max_threads = 15


class FindBot(BotCore):
    ChrTab = -1
    working = 0
    
    def __init__(self, item):
        FindBot.ChrTab += 1
        self.ChrTab = FindBot.ChrTab
        super().__init__(self.ChrTab)
        self.item = item

    def get_article(self, url):
        ptype, host, port, user, pwd = self.get_proxy()
        proxies = {
            'http' : '%s://%s:%s@%s:%d' % (ptype, user, pwd, host, port),
            'https' : '%s://%s:%s@%s:%d' % (ptype, user, pwd, host, port)
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/web'
                      'p,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'connection': 'keep-alive',
            'host': 'www.zip-2002.ru',
            'referer': self.URL,
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }
        r = self.session.get(url, headers=headers, proxies=proxies, timeout=10)
        if 'Артикул: ' not in r.text:
            raise RuntimeError('Не обнаржуен артикул на странице ' + url)
        return double_split(r.text, 'Артикул: ', '\n')

    def find(self):
        ptype, host, port, user, pwd = self.get_proxy()
        self.session = requests.Session()
        self.session.max_redirects = 3
        proxies = {
            'http': '%s://%s:%s@%s:%d' % (ptype, user, pwd, host, port),
            'https': '%s://%s:%s@%s:%d' % (ptype, user, pwd, host, port)
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/'
                      'apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'connection': 'keep-alive',
            'host': 'www.zip-2002.ru',
            'referer': self.URL,
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5'
                          '37.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }
        self.url = f'http://www.zip-2002.ru/search/?query={self.item}'
        r = self.session.get(self.url, headers=headers, proxies=proxies, timeout=10)

        url_containers = r.text.split('class="product-box"')[1:]
        item_urls = {double_split(cont, '<a href="', '"'): 'В корзину' in cont
                     for cont in url_containers}
        for url, avail in item_urls.items():
            article = self.get_article(url)
            if article == self.item:
                if avail:
                    result[self.ChrTab] = 'ДОСТУПЕН!'
                else:
                    result[self.ChrTab] = 'Нет в наличии'
                lprint('#' + str(self.ChrTab) + ' ' + result[self.ChrTab])
                return
        else:
            result[self.ChrTab] = 'Товар не найден ботом!' + ';' + self.url
            lprint('#' + str(self.ChrTab) + ' ' + result[self.ChrTab])
    
    def run(self):
        self.URL = 'http://www.zip-2002.ru/'
        def to_try():
            FindBot.working += 1
            self.find()
            FindBot.working -= 1
        def to_except():
            FindBot.working -= 1
        if not multi_try(to_try, to_except, 'Main', 10, self.release, multiplier=1.08):
            result[self.ChrTab] = 'Ошибка во время выполнения' + ';' + self.url
            lprint('#' + str(self.ChrTab) + ' ' + result[self.ChrTab])

BotCore.max_tries = 3
BotCore.release = True

###-------------###
with open('input.txt', 'r', encoding='utf-8') as f:
    ininput = f.read()
items = ininput.split('\n')
items = [item.strip() for item in items]
items = [item.replace('Б', '%C1') for item in items]
###-------------###

items = items
print(items)
result = ['' for i in range(len(items))]
while items:
    if FindBot.working < max_threads:
        item = items.pop(0)
        bot = FindBot(item)
        bot.start()
    else:
        time.sleep(1)
else:
    time.sleep(1)
    while FindBot.working:
        time.sleep(1)
to_write = '\n'.join(result)
try:
    with open('output.txt', 'w+', encoding='utf-8') as f:
        to_write = to_write.encode('cp1251', 'ignore')
        to_write = to_write.decode('cp1251', 'ignore')
        f.write(to_write)
except:
    a = input('Попробовать еще раз')
    with open('output.txt', 'w+', encoding='utf-8') as f:
        to_write = '\n'.join(result)
        to_write = to_write.encode('cp1251', 'ignore')
        to_write = to_write.decode('cp1251', 'ignore')
        f.write(to_write)
print('--Граббинг завершен--')