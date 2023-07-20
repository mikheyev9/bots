import os
import sys

from cores_src.cores import *
from cores_src.vis import *


class ChromeTab(BotCore):
    def __init__(self, ChrTab):
        super().__init__(ChrTab)
        self.check_proxies('https://aviasales.ru/', personal=True, verify=False)


Tab = ChromeTab(0)
