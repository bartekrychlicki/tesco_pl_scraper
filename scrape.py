#!/usr/bin/env python3.4
from lib.tesco_scraper import TescoScraper

LINE_BUFFERED = 1


def main():
    with open('prices.csv', 'w', LINE_BUFFERED) as csv_file:
        TescoScraper().scrape_all_to_file(csv_file)

if __name__ == '__main__':
    main()
