import os
import random
import time

import requests
from DrissionPage import ChromiumPage, ChromiumOptions

from DrissionPage.common import Settings
from dotenv import load_dotenv

min_price = float('inf')
pre_min_price = float('inf')
name = ""
url = ""
pre_notify_time = 0


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

    def update_price(self):
        self.load_price_page()
        global min_price
        global name
        global url
        try:
            price = self.page.ele(".{}".format(self.class_name)).text
            price = float(price[1:].replace(',', ''))
            if price < min_price:
                min_price = price
                name = self.name
                url = self.url
        except Exception as e:
            print(e)

    @staticmethod
    def notify():
        global pre_notify_time
        global name
        global url
        if min_price < pre_min_price:
            text = "在{}发现新的最低价格:${},地址:{}".format(name, min_price, url)
        elif pre_notify_time + 24 * 3600_000 > int(round(time.time() * 1000)):
            pre_notify_time = int(round(time.time() * 1000))
            text = "价格未更新,最低价格仍然是:{},价格为:${}，地址:{}".format(name, min_price, url)
        else:
            return
        load_dotenv()
        WEBHOOK_URL = os.getenv('LARK_WEBHOOK_URL')
        requests.post(WEBHOOK_URL, json={
            "msg_type": "text",
            "content": {
                "text": text
            }
        })
        global pre_notify_time
        pre_notify_time = int(round(time.time() * 1000))

    # 创建静态方法
    @staticmethod
    def job(georges_monitor, digi_direct_monitor, teds_monitor):
        global pre_min_price
        pre_min_price = min_price
        georges_monitor.update_price()
        digi_direct_monitor.update_price()
        teds_monitor.update_price()
        Monitor.notify()
