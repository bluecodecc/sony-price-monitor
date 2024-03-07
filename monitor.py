import random

import requests
from DrissionPage import ChromiumPage, ChromiumOptions

from DrissionPage.common import Settings

min_price = float('inf')


class Monitor:
    def __init__(self, url, name, class_name):
        self.url = url
        self.name = name
        self.class_name = class_name
        chromium_options = ChromiumOptions()
        chromium_options.set_argument('--headless')
        chromium_options.set_argument('--no-sandbox')
        self.page = ChromiumPage(chromium_options)
        self.random = random.Random()
        Settings.raise_when_ele_not_found = True

    def load_price_page(self):
        self.page.get(self.url)
        self.page.wait.load_complete()
        # self.page.get_screenshot(path='./', name='pic.jpg', full_page=True)

    def get_price(self):
        self.load_price_page()
        global min_price
        try:
            price = self.page.ele(".{}".format(self.class_name)).text
            price = float(price[1:].replace(',', ''))
            if price < min_price:
                min_price = price
                self.notify()
        except Exception as e:
            print(e)

    def notify(self):
        requests.post('https://open.feishu.cn/open-apis/bot/v2/hook/f958efb6-3256-4a9c-a0e5-a12c60e2cd10', json={
            "msg_type": "text",
            "content": {
                "text": "The price of {} is ${} {}".format(self.name, min_price, self.url)
            }
        })
        print("The price of {} is ${}".format(self.name, min_price))

    # 创建静态方法
    @staticmethod
    def job(georges_monitor, digi_direct_monitor, teds_monitor):
        georges_monitor.get_price()
        digi_direct_monitor.get_price()
        teds_monitor.get_price()
