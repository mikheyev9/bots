import re
import string
import threading
from collections.abc import Iterable
from multiprocessing import Queue

from loguru import logger
from requests_toolbelt import MultipartEncoder
from selenium.webdriver.common.by import By

from cores_src.cores import *
from cores_src.main_utils import ProxySession
from cores_src.vis import *

MAX_THREADS = 1
LOGIN = 'hoztorg774@mail.ru'
PASSWORD = 'Serg75488659'
SHOP_ID = 11132


def login_kazan():
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHT' \
                 'ML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

    BotCore.blocking_hosts = ()
    BotCore.proxy_centralized = False
    bot_core = BotCore(4)
    session = ProxySession(bot_core)

    url = 'https://business.kazanexpress.ru/seller/signin'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,ima'
                  'ge/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '""',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user_agent,
    }
    r = session.get(url, headers=headers)

    jses = lrsplit(r.text, '<script src="', '"')
    basic_token = None
    enviroment_key = None
    louis_key = None
    for i, js in enumerate(jses[::-1]):
        blueprint(f'Поиск ключей авторизации {i}/{len(jses)}')
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '""',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': user_agent
        }
        url = 'https://business.kazanexpress.ru/' + js
        r = session.get(url, headers=headers)
        match1 = re.search(r',\w=\w\("fffc"\),\w="([a-zA-Z0-9=]+)"', r.text)
        if match1:
            basic_token = match1.group(1)
            basic_token = 'Basic ' + basic_token
            blueprint(f'Токен A обнаружен {basic_token}')
            if louis_key:
                continue
        elif 'VUE_APP_LOUIS_KEY:"' in r.text:
            louis_key = double_split(r.text, 'VUE_APP_LOUIS_KEY:"', '"')
            enviroment_key = double_split(r.text, 'VUE_APP_FLAGSMITH_ENV_ID:"', '"')
            blueprint(f'Токен B обнаружен {louis_key}')
            if basic_token:
                continue
        elif louis_key and basic_token:
            break
        else:
            continue
    else:
        raise RuntimeError('Сайт изменился, необходимо поменять авторизацию')

    url = 'https://flags.kazanexpress.ru/api/v1/flags/'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '""',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
        'X-Environment-Key': enviroment_key
    }
    r = session.get(url, headers=headers)

    url = 'https://api.business.kazanexpress.ru/api/oauth/token'
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'{basic_token}',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://business.kazanexpress.ru',
        'referer': 'https://business.kazanexpress.ru/',
        'sec-ch-ua': '',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '""',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
    }
    data = {
        'grant_type': 'password',
        'username': LOGIN,
        'password': PASSWORD,
    }
    r = session.post(url, headers=headers, data=data)
    bearer_token = r.json()['access_token']
    refresh_token = r.json()['refresh_token']

    url = 'https://api.business.kazanexpress.ru/api/oauth/token'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'access-control-request-headers': 'authorization',
        'access-control-request-method': 'POST',
        'origin': 'https://business.kazanexpress.ru',
        'referer': 'https://business.kazanexpress.ru/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
    }
    r = session.options(url, headers=headers)

    url = 'https://api.business.kazanexpress.ru/api/seller/verification'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'access-control-request-headers': 'authorization',
        'access-control-request-method': 'GET',
        'origin': 'https://business.kazanexpress.ru',
        'referer': 'https://business.kazanexpress.ru/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
    }
    r = session.options(url, headers=headers)

    url = 'https://api.business.kazanexpress.ru/api/seller/verification'
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {bearer_token}',
        'origin': 'https://business.kazanexpress.ru',
        'referer': 'https://business.kazanexpress.ru/',
        'sec-ch-ua': '',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '""',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
    }
    r = session.get(url, headers=headers)

    url = 'https://api.business.kazanexpress.ru/api/auth/seller/check_token'
    headers = {
       'accept': 'application/json',
       'accept-encoding': 'gzip, deflate, br',
       'accept-language': 'en-US,en;q=0.9',
       'authorization': basic_token,
       'content-length': '33',
       'content-type': 'application/x-www-form-urlencoded',
       'origin': 'https://business.kazanexpress.ru',
       'referer': 'https://business.kazanexpress.ru/',
       'sec-ch-ua': '',
       'sec-ch-ua-mobile': '?0',
       'sec-ch-ua-platform': '""',
       'sec-fetch-dest': 'empty',
       'sec-fetch-mode': 'cors',
       'sec-fetch-site': 'same-site',
       'user-agent': user_agent,
    }
    data = {
       'token': bearer_token,
    }
    r = requests.post(url, headers=headers, data=data)
    blueprint('Авторизация успешна')
    bearer_token = 'Bearer ' + bearer_token
    return session, basic_token, bearer_token, louis_key, refresh_token


class BasePipe(BotCore):
    results = Queue()
    tab = 0

    def __init__(self, items):
        BasePipe.tab += 1
        super().__init__(BasePipe.tab)
        self.item = None
        if isinstance(items, Iterable):
            self.queue = Queue()
            for item in items:
                self.queue.put(item)
        else:
            self.queue = items
        self.start()

    def get_prefix(self, item):
        return item

    def result(self, message, color=None):
        prefix = self.get_prefix(self.item)
        message = f'{prefix}: {message}'
        with open('results.txt', 'a', encoding='utf-8') as f:
            f.write(message)
        if color:
            message = colorize(message, color=color)
        print(message)

    def body(self):
        pass

    def run(self):
        while True:
            self.item = self.queue.get()
            if not multi_try(self.body, fpass, name='Main'):
                self.result('Ошибка во время исполнения', Fore.RED)


class FindWorker(BasePipe):
    results = Queue()

    def __init__(self, queue):
        super().__init__(queue)

    def body(self):
        url = 'https://autocomplete.diginetica.net/autocomplete'
        data = {
            'st': self.item,
            'apiKey': 'SPVZ9HCWL9',
            'strategy': 'advanced,zero_queries',
            'productsSize': '20',
            'regionId': 'global',
            'forIs': 'false',
            'showUnavailable': 'true',
            'withContent': 'false',
            'withSku': 'false'
        }
        r = requests.get(url, params=data)
        for product in r.json()['products']:
            if product['attributes']['vendorcode'][0] == str(self.item):
                self.results.put(['https://procontact74.ru' + product['link_url'], self.item])
                return
        else:
            self.result('Товар не был обнаружен на проконтакте', color=Fore.RED)


class LinkWorker(BasePipe):
    results = Queue()

    def __init__(self, queue):
        super().__init__(queue)

    def get_prefix(self, item):
        return item[1]

    def body(self):
        link, article = self.item
        r = requests.get(link)
        description = double_split(r.text, '<div class="description">', '</div>')
        image_url = double_split(r.text, 'class="minimized" src="', '"')
        image_url = 'https://procontact74.ru' + image_url
        image_content = download(image_url, save=False, temp=False)
        name = double_split(r.text, '<h1>', '</h1>')
        self.results.put([article, link, name, image_content, description])


class KazanWorker(BasePipe):
    session, basic_token, bearer_token, louis_key, refresh_token = login_kazan()

    def __init__(self, queue):
        super().__init__(queue)

    def get_prefix(self, item):
        return item[0]

    def check_sku(self, article):
        url = f'https://api.business.kazanexpress.ru/api/seller/shop/{SHOP_ID}/product/checkSku?sku={article}'
        headers = {
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.bearer_token,
            'origin': 'https://business.kazanexpress.ru',
            'referer': 'https://business.kazanexpress.ru/',
            'sec-ch-ua': '',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '""',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': self.user_agent,
        }
        r = self.session.get(url, headers=headers)
        return r.json()['exists']

    def init_new(self):
        url = f'https://business.kazanexpress.ru/seller/{SHOP_ID}/products/new/'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,ima'
                      'ge/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://business.kazanexpress.ru/',
            'sec-ch-ua': '',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '""',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent,
        }
        r = self.session.get(url, headers=headers)
        logger.debug(r.text)

    def upload_photo(self, image_content):
        boundary_chars = random.sample(string.ascii_letters + string.digits, 16)
        boundary_hash = ''.join(boundary_chars)
        url = 'https://louis.kznexpress.ru/upload'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.louis_key,
            'content-length': '146996',
            'origin': 'https://business.kazanexpress.ru',
            'referer': 'https://business.kazanexpress.ru/',
            'sec-ch-ua': '',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '""',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': self.user_agent,
        }
        fields = {
            'file': ('image.png', image_content, "image/png"),   # Точно ПНГ?
            'tags': 'product_3x4,product'
        }
        boundary = '----WebKitFormBoundary'
        data = MultipartEncoder(fields=fields, boundary=boundary)
        data = (f'------WebKitFormBoundary{boundary_hash}\n'
                'Content-Disposition: form-data; name="file"; filename="image.png"\n'
                f'Content-Type: image/png\n\n\n------WebKitFormBoundary{boundary_hash}\n'
                'Content-Disposition: form-data; name="tags"\n\nproduct_3x4,product\n'
                f'------WebKitFormBoundary{boundary_hash}--')
        files = {
            'file': ('image.jpeg', image_content, "image/jpeg"),
            'tags': 'product_3x4,product'
        }
        r = self.session.post(url, headers=headers, files=files)
        return r.json()

    def create_new(self, title, description, image_data):
        data = {
            "attributes": [],
            "blockReason": "",
            "blockedImages": {},
            "categoryEditable": True,
            "colorCollectionImages": [],
            "colorVideos": [],
            "comments": [],
            "customCharacteristics": [],
            "dateModerated": None,
            "definedCharacteristics": [],
            "description": description,
            "filterValues": [{"filterId": 6, "filterValueId": 200057}],
            "filters": [],
            "imageCollection": None,
            "okpd2": None,
            "photoOnPreview": False,
            "productFields": {},
            "productImages": [
                {
                    "deletable": True,
                    "url": image_data['payload']['originalUrl'],
                    "key": image_data['payload']['key'],
                    "status": "ACTIVE",
                }
            ],
            "ratingInfo": None,
            "shortDescription": format_descr(description)[:380],
            "skuBlockReason": None,
            "title": title,
            "video": None,
            "vat": "VAT20",
            "categoryId": 11756
        }
        url = f'https://api.business.kazanexpress.ru/api/seller/shop/{SHOP_ID}/product/createProduct'
        headers = {
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.bearer_token,
            'content-type': 'application/json',
            'origin': 'https://business.kazanexpress.ru',
            'referer': 'https://business.kazanexpress.ru/',
            'sec-ch-ua': '',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '""',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': self.user_agent,
        }
        r = self.session.post(url, headers=headers, json=data)
        logger.debug(r.text)
        if 'id' not in r.json():
            print('Ошибка создания товара', Fore.RED)
        return r.json()

    def send_sku(self, product_data, article):
        data = {
            "productId": product_data['id'],
            "skuForProduct": str(article),
            "skuList": [
                {
                    "fullPrice": 9999,
                    "sellPrice": 9999,
                    "skuTitle": f"{product_data['shopSkuTitle']}-{article}",
                    "barcode": None,
                    "skuCharacteristicList": [],
                    "status": None,
                }
            ],
            "skuTitlesForCustomCharacteristics": [],
        }
        url = f'https://api.business.kazanexpress.ru/api/seller/shop/{SHOP_ID}/product/sendSkuData'
        headers = {
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.bearer_token,
            'content-length': '216',
            'content-type': 'application/json',
            'origin': 'https://business.kazanexpress.ru',
            'referer': 'https://business.kazanexpress.ru/',
            'sec-ch-ua': '',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '""',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': self.user_agent,
        }
        r = self.session.post(url, headers=headers, json=data)
        return r.text

    def body(self):
        article, link, name, image_content, description = self.item
        if self.check_sku(article):
            self.result('Товар с таким артикулом уже есть')
            return
        self.init_new()
        photo_data = self.upload_photo(image_content)
        if 'payload' not in photo_data:
            self.result('Ошибка отправки изображения. Изображение на проконтакте, вероятно, не JPEG',
                        Fore.RED)
            return
        data = self.create_new(name, description, photo_data)
        response = self.send_sku(data, article)
        if not response:
            self.result('Успешно добавлен!')
        else:
            self.result(f'Ошибка SKU, однако карточка товара создана: {response}', color=Fore.RED)


def format_descr(description):
    description = description.replace('<br/>', '\n')
    return description


if __name__ == "__main__":
    with open('input.txt') as f:
        items = [row for row in f.read().split('\n') if row]
    stage1 = FindWorker(items)
    stage2 = LinkWorker(stage1.results)
    stage3 = KazanWorker(stage2.results)
    main_result = stage3.results.get()
    print(main_result)
