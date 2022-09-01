import logging
import pickle
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import configs_shops.config_dns

OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument(configs_shops.config_dns.ua)
OPTIONS.add_argument(configs_shops.config_dns.webdriver_disable)
OPTIONS.headless = True
SERVICE = Service(executable_path='/home/vladimir/Pythonproject/parser-vc/configs_shops/chromedriver')
DRIVER = webdriver.Chrome(service=SERVICE, options=OPTIONS)


def get_data_dns() -> dict:
    '''
    :param pages:
    :return dict :
    Функция парсит сайт dns-shop.ru на поиск доступных видеокарт по определенным фильтрам
    '''

    product_result_dns = {}
    product_num = 0
    pages = get_pages()
    for page in range(1, pages + 1):
        try:
            DRIVER.get(f'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?p={page}')
            time.sleep(2)
            prods = DRIVER.find_elements(By.CLASS_NAME, 'catalog-product')
            for prod in prods:
                if 'RTX' in prod.find_element(By.CLASS_NAME, 'catalog-product__name').text and \
                        'В наличии' in prod.find_element(By.CLASS_NAME, 'catalog-product__avails').text.split('\n')[0]:
                    product_num += 1
                    product_result_dns[product_num] = {
                        'product_name': prod.find_element(By.CLASS_NAME, 'catalog-product__name').text,
                        'product_link': prod.find_element(By.CLASS_NAME, 'catalog-product__name').get_attribute('href'),
                        'product_price': prod.find_element(By.CLASS_NAME, 'catalog-product__buy').text.split('\n')[0],
                        'product_available': 1
                    }
        except Exception as ex:
            logging.exception(msg=ex)
    DRIVER.close()
    DRIVER.quit()
    return product_result_dns


def get_pages() -> int:
    '''
    Функция предназначена для поиска количества страниц пагинации и загрузки печенек
    '''

    DRIVER.get('https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/')
    for cook in pickle.load(open('configs_shops/cookies_dns', 'rb')):
        DRIVER.add_cookie(cook)
    time.sleep(2)
    DRIVER.refresh()

    pages_count_link = DRIVER.find_element(By.CLASS_NAME, 'pagination-widget__page-link_last')
    pages_count = int(re.findall(r'p=(\d\d)', str(pages_count_link.get_attribute('href')))[0])
    return pages_count


def main():
    get_data_dns()


if __name__ == '__main__':
    main()
