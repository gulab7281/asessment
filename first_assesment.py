import requests
import bs4
from pymongo import MongoClient


def product():
    for page in range(1, 6):
        url = 'https://www.bukalapak.com/products?page=' + str(page) + '&search%5Bkeywords%5D=samsung'
        req_data = requests.get(url)
        bs_object = bs4.BeautifulSoup(req_data.content)

        all_data = bs_object.find_all('div', attrs={'class': "bl-flex-container flex-wrap is-gutter-16"})
        all_phone = all_data[0].find_all('div', attrs={'class': "bl-flex-item mb-8"})
        for phone in all_phone:
            product_dict = {}
            name_and_url = phone.find('p', attrs={'class': "bl-text bl-text--body-14 bl-text--ellipsis__2"})
            name_and_url_ = name_and_url.find('a')
            product_name = name_and_url_.text.strip()
            product_dict['Product_name'] = product_name

            product_url = name_and_url_['href']
            product_dict['Product_url'] = product_url

            product_price_ = phone.find('p', attrs={
                'class': "bl-text bl-text--subheading-20 bl-text--semi-bold bl-text--ellipsis__1"})
            product_price = product_price_.text.strip()
            product_price = product_price.replace('Rp', '')
            product_dict['Product_price'] = product_price

            product_rating_data = phone.find_all('p', attrs={'class', "bl-text bl-text--body-14 bl-text--subdued"})
            for product_rat in product_rating_data:
                product_rating_ = product_rat.find('a', attrs={'class': "bl-link"})
                if product_rating_ is not None:
                    product_rating = product_rating_.text.strip()
                    product_dict['Product_rating'] = product_rating
            location_data = phone.find('div', attrs={'class': "bl-product-card__description-store"})
            location = location_data.text.strip()
            product_dict['Location'] = location
            product_dict['Brand'] = 'SAMSUNG'

            ## insert jsondata in mongodb
            client = MongoClient('fill mongodb_ip')
            database_ = client['fill mongodb_database']
            client.server_info()
            table_ = database_["fill table name"]
            table_.create_index("fill one key_name in json for filter", unique=True)
            table_.insert_one(product_dict)
            print("Sucessfully insert json data")
