import os
from itertools import product
import json
import requests
from bs4 import BeautifulSoup as BS
from multiprocessing import Pool
from tqdm import tqdm

# URL = 'https://www.kivano.kg/elektronika'
# URL = 'https://www.kivano.kg/noutbuki'


def get_html(url: str) -> str:
    html = requests.get(url = url).text
    return html
    
# html = get_html(url=URL)
def get_data(html: str):
    soup = BS(html, 'lxml')
    data = soup.find('div', class_='list-view')
    products = data.find_all('div', class_='item')
    return products

# html = get_html(url=URL)
# data = get_data(html=html)

def convert_usd(money: str) -> str:
    result = round(int(money.split()[0])/85, 2)
    return str(result) + '$'
def write_json(data):
    with open('info.json', 'a') as file:
        json.dump(data, file, ensure_ascii=False, indent = 2)


def main(data: list):
    products_list = list()
    for product in tqdm(data):
        try:
            title = product.find('div', class_='pull-right').find('div', class_='product_text').find('strong').find('a').text
        except:
            title = '-'
        # print(title)
        try:
            desc = product.find('div', class_='pull-right').find('div', class_='product_text').text
        except:
            desc = '-'
        # print(desc)
        try:
            price = product.find('div', class_='pull-right').find('div', class_='motive_box').find('div', class_='listbox_price').text
        except:
            price = '-'
        
        price = convert_usd(price)

        new_product = {'title': title, 
                    'desc': desc,
                    'price': price}
        products_list.append(new_product)
    write_json(data = products_list)
# main(data=data)
def fast_pars(url:str):
    html = get_html(url=url)
    data = get_data(html=html)
    main(data=data)

def start():
    URL = 'https://www.kivano.kg/smart-chasy-i-fitnes-braslety'
    # URL = 'https://www.kivano.kg/mobilnye-telefony'
    page = '?page='
    urls = [URL + page + str(i) for i in range(1,56)]
    with Pool(os.cpu_count()) as p:
        p.map(fast_pars, urls)

start()

    # html = get_html(url=URL)
    # data = get_data(html=html)
    # main(data=data)
