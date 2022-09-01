import requests
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from asyncio import run

from configs_shops import config_cl


def get_data_cl() -> dict:
    '''
    Функция парсит сайт citilink.ru на поиск доступных видеокарт по определенным фильтрам
    '''
    with requests.Session() as session_cl:
        product_result_cl = {}
        product_num = 0
        response = session_cl.get(
            'https://www.citilink.ru/catalog/videokarty/?pf=available.all%2Cavailable.instore%2Cdiscount.any%2Crating.any%2C9368_29nvidiad1d1geforced1rtxd12060%2C9368_29nvidiad1d1geforced1rtxd12060super%2C9368_29nvidiad1d1geforced1rtxd13050%2C9368_29nvidiad1d1geforced1rtxd13060%2C9368_29nvidiad1d1geforced1rtxd13060ti%2C9368_29nvidiad1d1geforced1rtxd13070%2C9368_29nvidiad1d1geforced1rtxd13070ti%2C9368_29nvidiad1d1geforced1rtxd13080%2C9368_29nvidiad1d1geforced1rtxd13080ti%2C9368_29nvidiad1d1geforced1rtxd13090%2C9368_29nvidiad1d1geforced1rtxd13090ti&f=available.instore%2Cdiscount.any%2Crating.any%2C9368_29nvidiad1d1geforced1rtxd12060%2C9368_29nvidiad1d1geforced1rtxd12060super%2C9368_29nvidiad1d1geforced1rtxd13050%2C9368_29nvidiad1d1geforced1rtxd13060%2C9368_29nvidiad1d1geforced1rtxd13060ti%2C9368_29nvidiad1d1geforced1rtxd13070%2C9368_29nvidiad1d1geforced1rtxd13070ti%2C9368_29nvidiad1d1geforced1rtxd13080%2C9368_29nvidiad1d1geforced1rtxd13080ti%2C9368_29nvidiad1d1geforced1rtxd13090%2C9368_29nvidiad1d1geforced1rtxd13090ti&sorting=price_asc',
            headers=config_cl.headers_cl)

        response_pages_count_text = response.text
        pages_count = get_pages(response_pages_count_text)
        for page in range(1, pages_count + 1):
            response = session_cl.get(
                f"https://www.citilink.ru/catalog/videokarty/?pf=available.all%2Cavailable.instore%2Cdiscount.any%2Crating.any%2C9368_29nvidiad1d1geforced1rtxd12060%2C9368_29nvidiad1d1geforced1rtxd12060super%2C9368_29nvidiad1d1geforced1rtxd13050%2C9368_29nvidiad1d1geforced1rtxd13060%2C9368_29nvidiad1d1geforced1rtxd13060ti%2C9368_29nvidiad1d1geforced1rtxd13070%2C9368_29nvidiad1d1geforced1rtxd13070ti%2C9368_29nvidiad1d1geforced1rtxd13080%2C9368_29nvidiad1d1geforced1rtxd13080ti%2C9368_29nvidiad1d1geforced1rtxd13090%2C9368_29nvidiad1d1geforced1rtxd13090ti&f=available.instore%2Cdiscount.any%2Crating.any%2C9368_29nvidiad1d1geforced1rtxd12060%2C9368_29nvidiad1d1geforced1rtxd12060super%2C9368_29nvidiad1d1geforced1rtxd13050%2C9368_29nvidiad1d1geforced1rtxd13060%2C9368_29nvidiad1d1geforced1rtxd13060ti%2C9368_29nvidiad1d1geforced1rtxd13070%2C9368_29nvidiad1d1geforced1rtxd13070ti%2C9368_29nvidiad1d1geforced1rtxd13080%2C9368_29nvidiad1d1geforced1rtxd13080ti%2C9368_29nvidiad1d1geforced1rtxd13090%2C9368_29nvidiad1d1geforced1rtxd13090ti&sorting=price_asc&p={page}",
                headers=config_cl.headers_cl
            )
            response_text = response.text
            soup = BeautifulSoup(response_text, 'lxml')
            prods = [prod for prod in soup.find_all('div', class_='product_data__gtm-js')]
            for prod in prods:
                product_num += 1
                product_result_cl[product_num] = {
                    'product_name': prod.find('a', 'ProductCardHorizontal__title').text.strip(),
                    'product_link': f"https://www.citilink.ru{prod.find('a', 'ProductCardHorizontal__title').get('href')}",
                    'product_price': prod.find('span', 'ProductCardHorizontal__price_current-price').text.strip(),
                    'product_available': 1
                }
        return product_result_cl


def get_pages(response_pages_count_text: str) -> int:
    '''Функция предназначена для поиска страниц пагинации'''
    soup = BeautifulSoup(response_pages_count_text, 'lxml')
    pages_count_link = soup.find_all('a', class_='PaginationWidget__page')
    if pages_count_link:
        return int(pages_count_link[-1].text.strip())
    else:
        return 1


def main():
    get_data_cl()


if __name__ == '__main__':
    main()
