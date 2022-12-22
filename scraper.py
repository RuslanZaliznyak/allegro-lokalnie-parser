import csv
import json

import requests
from bs4 import BeautifulSoup
from typing import NamedTuple


class Offer(NamedTuple):
    title: str
    price: str
    url: str
    offer_type: str


class Parser:
    def __init__(self, item_name, file_name):
        self.main_url = f'https://allegrolokalnie.pl'
        self.offer_page = f'https://allegrolokalnie.pl/oferty/q/{item_name}'
        self.page = 1
        self.file_name = file_name

    def create_session(self):
        session = requests.Session()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.1; WOW64; en-US) Gecko/20100101 Firefox/74.7',
            'Accept-Language': 'uk-UA, uk;q=0.9, en;q=0.8'
        }
        session.headers.update(headers)

        session.verify = True
        session.timeout = 30

        return session

    def get_data_from_site(self, page):
        session = self.create_session()
        req = session.get(f'{self.offer_page}?page={page}')
        if req.status_code == 200:
            return req.content

    def get_page_count(self) -> int:
        try:
            get_src = self.get_data_from_site(self.page)
            main_page_src = get_src
            soup = BeautifulSoup(main_page_src, 'lxml')
            pagination_element = soup.find(attrs={'data-mlc-listing-bottom-pagination': True})
            if pagination_element:
                pagination_data = pagination_element['data-mlc-listing-bottom-pagination']
                pagination_dict = json.loads(pagination_data)
                return int(pagination_dict['pages_count'])
        except Exception as e:
            print(f"Error occurred while fetching page count: {str(e)}")
            return 0

    def get_product_data_from_pages(self):
        page_count = self.get_page_count()

        if page_count == 0:
            print("No data to fetch.")
            return []

        offers_result = []
        try:
            for page in range(page_count + 1):
                page_src = self.get_data_from_site(page)

                soup = BeautifulSoup(page_src, 'lxml')

                if soup is not None:
                    try:
                        offer_list = soup.find('div', attrs={'data-testid': 'offers-list'})
                        all_offers = offer_list.find_all('article', attrs={'itemtype': "http://schema.org/Offer"})
                    except AttributeError:
                        break

                    for offer in all_offers:
                        try:
                            title = offer.find('div', class_='mlc-itembox__body-header').text
                            url = offer.find('a').get('href')
                        except AttributeError:
                            continue

                        try:
                            price = offer.find('div', class_='mlc-itembox__price').text
                            offer_type = offer.find('span', class_='mlc-itembox__offer-type').text
                        except AttributeError:
                            price = None
                            offer_type = None

                        title_ = title.replace('\n', '').strip()
                        price_ = price.replace('\xa0', '').replace('\n', '').strip()
                        url_ = f'{self.main_url}{url}'
                        offer_type_ = offer_type.strip()

                        offer_obj = Offer(title=title_,
                                          price=price_,
                                          url=url_,
                                          offer_type=offer_type_)
                        offers_result.append(offer_obj)

                    self.page = page + 1
        except Exception as e:
            print(f"Error occurred while fetching product data: {str(e)}")

        return offers_result

    def save_to_csv(self):
        try:
            offers_result = self.get_product_data_from_pages()

            with open(self.file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Title', 'Price', 'URL', 'Offer Type'])

                for offer in offers_result:
                    writer.writerow([offer.title, offer.price, offer.url, offer.offer_type])
        except Exception as e:
            print(f"Error occurred while saving data to CSV: {str(e)}")
