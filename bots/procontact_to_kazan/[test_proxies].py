from cores_src.cores import *
from cores_src.vis import *


class ChromeTab(BotCore):
    def __init__(self, tab_num):
        super().__init__(tab_num)
        self.check_proxies('https://business.kazanexpress.ru/seller/signin', personal=True, verify=False)


if __name__ == '__main__':
    tab = ChromeTab(0)
