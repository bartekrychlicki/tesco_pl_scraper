#!/usr/bin/env python3
import urllib.request
import sys
import re
from pyquery import PyQuery
import urllib
import csv

RE_CAT_IDS = '=P1_Cat(\d+)'
MAIN_URL = 'http://ezakupy.tesco.pl'
CAT_URL = 'http://ezakupy.tesco.pl/pl-PL/Product/BrowseProducts?taxonomyId=Cat'
LINE_BUFFERED = 1


def read_url(url):
    user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, '
                  'like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0'
                  '.1025.168 Safari/535.19')
    u = urllib.request.urlopen(urllib.request.Request(url, headers={
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,imag'
                  'e/webp,*/*;q=0.8'
        }))
    return u.read().decode('utf-8')


def get_main_cats():
    return re.findall(RE_CAT_IDS, read_url(MAIN_URL))


def scrap_cat(cat_id):
    ret = []
    index = 1
    while True:
        cat_url = '{cat_url}{cat_id}&pageNo={index}'.format(
            cat_url=CAT_URL, cat_id=cat_id, index=index)
        dd = PyQuery(cat_url, opener=read_url)
        print(cat_url, cat_id)
        print()
        titles = dd('.cf.content').find('h2 a')
        prices = dd('.cf.content').find('.linePrice')
        assert len(titles) == len(prices)
        if not titles:
            break
        for title, price in zip(titles, prices):
            title = title.get('title') or title.text_content() or ''
            print(title.strip(), price.text.strip())
            ret.append((title.strip(), price.text.strip()))
            print()
        index += 1
    return ret


def main():
    with open('prices.csv', 'w', LINE_BUFFERED) as csf_vile:
        csv_writer = csv.writer(csf_vile)
        main_cats = get_main_cats()
        assert len(main_cats) > 0, '[ERR ] No categories found'
        for cat_id in main_cats:
            titles = scrap_cat(cat_id)
            csv_writer.writerows(titles)


if __name__ == '__main__':
    print("This scraper is deprecated, the TESCO website changed but scraper didn't catch up.")
    sys.exit(main())
