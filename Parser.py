import requests
import random

from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup



def user_agent(word):
    user_agents = ['Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36']
    url_new = f"https://omsk.uteka.ru/search/?query={word}&ac=text&sort=sort-rating&direction=desc"
    HEADER = {'User-Agent': random.choice(user_agents)}
    page = requests.get(url_new, data=HEADER)
    return page

def parse(word):
    medical_list = list()
    connect = user_agent(word)
    if connect.status_code == 200:
        soup = BeautifulSoup(connect.text, "html.parser")
        all_medicines = soup.findAll('div', class_="product-preview ui-panel ui-panel_size_s ui-panel_clickable")
        all_url = soup.findAll('div', class_="product-preview__inner")
        for medicine, url_data in zip(all_medicines, all_url):
            try:
                all_image = medicine.find("link", {"itemprop": "image"}).get("href")
                image_url = f"https://omsk.uteka.ru/{all_image}"
                names = medicine.find('span', {'itemprop': 'name'}).text
                cost = medicine.find('div', {'class': 'ui-price__content'}).text
                medicine_url = url_data.find("a", {"itemprop":"url"}).get("href")
                base_url = "https://omsk.uteka.ru"
                url = base_url + medicine_url
                medical = {'name': names, 'cost': cost, 'image_url': image_url, 'url': url}
                medical_list.append(medical)
            except AttributeError as e:
                print(e)
        return  medical_list


def parse_errors(word):
    text = (f'По вашему запросу «{word}» ничего не найдено').split()
    connect = user_agent(word)
    print(0)
    if connect.status_code == 200:
        print(3)
        soup = BeautifulSoup(connect.text, "html.parser")
        error_find = soup.findAll('div', class_="search-page__empty ui-container ui-container_size_l")
        for data in error_find:
            try:
                print(2)
                error = data.find('div', {'class': 'ui-placeholder__title ui-title ui-title_size_m ui-title_type_low ui-title_responsive'}).text.split()
                if error == text:
                    return False
                else:
                    print(1)
                    return True
            except AttributeError:
                return False
        return True