import logging
import re
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from configs_shops.config_cu import ua, webdriver_disable

OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument(ua)
OPTIONS.add_argument(webdriver_disable)
OPTIONS.headless = True
SERVICE = Service(executable_path='/home/vladimir/Pythonproject/parser-vc/configs_shops/chromedriver')
DRIVER = webdriver.Chrome(service=SERVICE, options=OPTIONS)
url = 'https://www.computeruniverse.net/ru/c/apparatnoe-obespechenie-i-komponenty/videokarty-nvidia?refinementList%5Bfacets.Chipsatz.values%5D%5B0%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203060%20Ti&refinementList%5Bfacets.Chipsatz.values%5D%5B1%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203070%20Ti%20%28LHR%29&refinementList%5Bfacets.Chipsatz.values%5D%5B2%5D=NVIDIA%C2%AE%20GeForce%C2%AE%20RTX%202060%20Super%E2%84%A2&refinementList%5Bfacets.Chipsatz.values%5D%5B3%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203070&refinementList%5Bfacets.Chipsatz.values%5D%5B4%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203080%20Ti%20%28LHR%29&refinementList%5Bfacets.Chipsatz.values%5D%5B5%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203060&refinementList%5Bfacets.Chipsatz.values%5D%5B6%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203080&refinementList%5Bfacets.Chipsatz.values%5D%5B7%5D=NVIDIA%C2%AE%20GeForce%C2%AE%20RTX%203090%20Ti&refinementList%5Bfacets.Chipsatz.values%5D%5B8%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203080%20Ti&refinementList%5Bfacets.Chipsatz.values%5D%5B9%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%202060&refinementList%5Bfacets.Chipsatz.values%5D%5B10%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203090&refinementList%5Bfacets.Chipsatz.values%5D%5B11%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203060%20%28LHR%29&refinementList%5Bfacets.Chipsatz.values%5D%5B12%5D=NVIDIA%C2%AE%20GeForce%C2%AE%20RTX%203050&refinementList%5Bfacets.Chipsatz.values%5D%5B13%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203080%20%28LHR%29&refinementList%5Bfacets.Chipsatz.values%5D%5B14%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203070%20%28LHR%29&refinementList%5Bfacets.Chipsatz.values%5D%5B15%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203070%20Ti&refinementList%5Bfacets.Chipsatz.values%5D%5B16%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203060%20Ti%20%28LHR%29&toggle%5Bdeliverydatenow%5D=true'


def get_data_cu() -> dict:
    '''
    :param pages:
    :return dict :

    Функция парсит сайт computeruniverse.net на поиск доступных видеокарт по определенным фильтрам
    '''

    product_result_cu = {}
    product_num = 0
    pages = get_pages()
    for page in range(1, pages + 1):
        num = 0
        try:
            DRIVER.get(
                f'https://www.computeruniverse.net/ru/c/apparatnoe-obespechenie-i-komponenty/videokarty-nvidia?refinementList%5Bfacets.Chipsatz.values%5D%5B0%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203060%20Ti&refinementList%5Bfacets.Chipsatz.values%5D%5B1%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203070%20Ti%20%28LHR%29&refinementList%5Bfacets.Chipsatz.values%5D%5B2%5D=NVIDIA%C2%AE%20GeForce%C2%AE%20RTX%202060%20Super%E2%84%A2&refinementList%5Bfacets.Chipsatz.values%5D%5B3%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203070&refinementList%5Bfacets.Chipsatz.values%5D%5B4%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203080%20Ti%20%28LHR%29&refinementList%5Bfacets.Chipsatz.values%5D%5B5%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203060&refinementList%5Bfacets.Chipsatz.values%5D%5B6%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203080&refinementList%5Bfacets.Chipsatz.values%5D%5B7%5D=NVIDIA%C2%AE%20GeForce%C2%AE%20RTX%203090%20Ti&refinementList%5Bfacets.Chipsatz.values%5D%5B8%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203080%20Ti&refinementList%5Bfacets.Chipsatz.values%5D%5B9%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%202060&refinementList%5Bfacets.Chipsatz.values%5D%5B10%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203090&refinementList%5Bfacets.Chipsatz.values%5D%5B11%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203060%20%28LHR%29&refinementList%5Bfacets.Chipsatz.values%5D%5B12%5D=NVIDIA%C2%AE%20GeForce%C2%AE%20RTX%203050&refinementList%5Bfacets.Chipsatz.values%5D%5B13%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203080%20%28LHR%29&refinementList%5Bfacets.Chipsatz.values%5D%5B14%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203070%20%28LHR%29&refinementList%5Bfacets.Chipsatz.values%5D%5B15%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203070%20Ti&refinementList%5Bfacets.Chipsatz.values%5D%5B16%5D=NVIDIA%C2%AE%20GeForce%20RTX%E2%84%A2%203060%20Ti%20%28LHR%29&toggle%5Bdeliverydatenow%5D=true&page={page}'
            )
            time.sleep(2)
            for _ in range(1, 18):
                DRIVER.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                time.sleep(0.15)

            prods = DRIVER.find_elements(By.CLASS_NAME, 'ais-Hits-item')
            for prod in prods:
                product_num += 1
                num += 1
                product_result_cu[product_num] = {
                    'product_name': prod.find_element(By.CLASS_NAME, 'ProductListItemRow_head__name___YFPb').text,
                    'product_link': prod.find_element(By.XPATH,
                                                      f'//*[@id="main-content"]/div/div[1]/div[2]/div[2]/div[6]/div/ul/li[{num}]/div/div[1]/div[1]/a').get_attribute(
                        'href'),
                    'product_price': [prod for prod in prod.find_element(By.XPATH,
                                                                         f'//*[@id="main-content"]/div/div[1]/div[2]/div[2]/div[6]/div/ul/li[{num}]/div/div[3]/div[2]/div[1]').text.split(
                        '\n') if '₽' in prod][0],
                    'product_available': 1
                }
        except Exception as ex:
            logging.exception(msg=ex)

    DRIVER.close()
    DRIVER.quit()
    return product_result_cu


def get_pages() -> int:
    '''
    Функция предназначена для поиска количества страниц пагинации
    '''
    DRIVER.get(url)
    time.sleep(2)
    pages_count_link = DRIVER.find_elements(By.CLASS_NAME, 'Pagination__naviButton__inner')[-2].get_attribute('href')
    pages_count = int(re.findall(r'page=(\d*)', pages_count_link)[0])
    return pages_count


def main():
    get_data_cu()


if __name__ == '__main__':
    main()