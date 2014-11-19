#!/usr/bin/env python3.4
import re
import csv
import urllib.request

from pyquery import PyQuery

from urls import UrlGenerator

LINE_BUFFERED = 1
RE_CAT_IDS = re.compile(r'=P1_Cat(\d+)')
USER_AGENT = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, '
              'like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0'
              '.1025.168 Safari/535.19')


class TitlesPricesNumbersDoNotMatchException(Exception):
    pass


def read_url(url):
    request = urllib.request.Request(url)
    request.add_header('User-Agent', USER_AGENT)
    request.add_header(
        'Accept',
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;'
        'q=0.8'
    )
    u = urllib.request.urlopen(request)
    return u.read().decode('utf-8')


def get_main_cats():
    return RE_CAT_IDS.findall(read_url(UrlGenerator.get_homepage()))


def scrap_cat(cat_id):
    ret = []
    index = 1
    while True:
        cat_url = UrlGenerator.make_category_url(cat_id, index)
        dd = PyQuery(cat_url, opener=read_url)
        print(cat_url, cat_id, '\n')
        titles = dd('.cf.content').find('h2 a')
        prices = dd('.cf.content').find('.linePrice')
        if len(titles) != len(prices):
            raise TitlesPricesNumbersDoNotMatchException
        if not titles:
            break
        for title, price in zip(titles, prices):
            title = title.get('title') or title.text_content()
            title = title.strip()
            price = price.text.strip()
            ret.append((title, price))
            print(title, price, '\n')
        index += 1
    return ret


def main():
    with open('prices.csv', 'w', LINE_BUFFERED) as csv_file:
        csv_writer = csv.writer(csv_file)
        main_cats = get_main_cats()
        for cat_id in main_cats:
            products = scrap_cat(cat_id)
            csv_writer.writerows(products)


if __name__ == '__main__':
    main()
