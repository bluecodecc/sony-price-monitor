import time

import schedule

from monitor import Monitor

if __name__ == '__main__':
    georges_monitor = Monitor("https://www.georges.com.au/products/sony-fe-70-200mm-f2-8-gm-m2-lens", "georges",
                              "price-item price-item--sale price-item--last")
    digi_direct_monitor = Monitor("https://www.digidirect.com.au/sony-fe-70-200mm-f-2-8-gm-m2-lens", "digidirect",
                                  "price")
    teds_monitor = Monitor("https://www.teds.com.au/sony-fe-70-200mm-f2-8-gm-m2-oss", "teds", "price")
    schedule.every(5).minutes.do(Monitor.job, georges_monitor, digi_direct_monitor, teds_monitor)
    while True:
        schedule.run_pending()
        time.sleep(1)
