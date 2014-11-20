import re
import csv
import itertools

from pyquery import PyQuery

from lib.connection import UrlMaker
from lib.connection import Connector


class NoDataOnPageException(Exception):
    pass


class TitlePriceNumbersMismatchError(Exception):
    pass


class TescoScraper(object):
    RE_CAT_IDS = re.compile(r'=P1_Cat(\d+)')

    @classmethod
    def scrape_all_to_file(cls, file):
        csv_writer = csv.writer(file)
        for products in cls.scrape_main_categories():
            csv_writer.writerow(products)

    @classmethod
    def scrape_main_categories(cls):
        main_cats = cls.get_main_categories()
        yield from cls.scrape_categories(main_cats)

    @classmethod
    def get_main_categories(cls):
        homepage = Connector.read_url(UrlMaker.get_homepage())
        return cls.RE_CAT_IDS.findall(homepage)

    @classmethod
    def scrape_categories(cls, categories):
        for cat_id in categories:
            yield from cls.scrape_category(cat_id)

    @classmethod
    def scrape_category(cls, cat_id):
        for index in itertools.count():
            page = cls.download_category_page(cat_id, index)
            try:
                yield from cls.extract_title_price_pairs(page)
            except NoDataOnPageException:
                break

    @staticmethod
    def download_category_page(cat_id, page_no):
        cat_url = UrlMaker.make_category_url(cat_id, page_no)
        print(cat_url, cat_id, end='\n\n')
        return PyQuery(cat_url, opener=Connector.read_url)

    @classmethod
    def extract_title_price_pairs(cls, pq_instance):
        # making these lists is dumb, but required for the below condition
        titles = list(cls.extract_titles(pq_instance))
        prices = list(cls.extract_prices(pq_instance))

        if len(titles) != len(prices):
            raise TitlePriceNumbersMismatchError
        if not titles:
            raise NoDataOnPageException

        for pair in zip(titles, prices):
            print(*pair)
            yield pair

    @staticmethod
    def extract_titles(pq_instance):
        titles = pq_instance('.cf.content').find('h2 a')
        for title in titles:
            title = title.get('title') or title.text_content()
            title = title.strip()
            yield title

    @staticmethod
    def extract_prices(pq_instance):
        prices = pq_instance('.cf.content').find('.linePrice')
        for price in prices:
            yield price.text.strip()
