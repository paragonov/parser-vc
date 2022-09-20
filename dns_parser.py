import re

import requests
from bs4 import BeautifulSoup

from configs_shops import config_dns


def scraper_dns():
    """
    Функция парсит сайт dns-shop.ru на поиск доступных видеокарт по определенным фильтрам
    """

    # Создаем сессию
    with requests.Session() as session:
        product_result_dns = {}

        # Получаем кол-во страниц пагинации через атрибут href и ищем число при помощи регулярки
        response_pagination = session.get(config_dns.url_dns, cookies=config_dns.cookies_dns,
                                          headers=config_dns.headers_dns)
        soup_pagination = BeautifulSoup(response_pagination.text, 'lxml')
        elem_pagination = soup_pagination.find_all('a',
                                                   class_='pagination-widget__page-link pagination-widget__page-link_last')
        # Регулярка
        pages_count = int(re.findall(r'p=(\d*)', str(elem_pagination[0].get('href')))[0])

        # Создаем списки с именами, ценами и доступности
        products_name = []
        products_price = []
        products_available = []

        # Проходим по полученным страницам
        for page in range(1, pages_count + 1):

            # Делаем запрос к текущей странице page
            response = session.get(f'{config_dns.url_dns}&p={page}', cookies=config_dns.cookies_dns,
                                   headers=config_dns.headers_dns)

            # Получаем страницу с 18 товарами, без блока цен и блока доступности
            soup = BeautifulSoup(response.text, 'lxml')

            # Добавляем в список имя товара
            products_name.extend(soup.find_all('a', class_='catalog-product__name ui-link ui-link_black'))

            # Находим все id товара
            product_id1 = soup.find_all('span', class_='catalog-product__buy product-buy')
            product_id2 = soup.find_all('div', class_='catalog-product ui-button-widget')

            # Группируем id. Поскольку у 1 товара 2 id, нам нужно их сгруппировать, чтобы потом составить data-строку
            products_ids = list(zip(product_id1, product_id2))

            # Создаем списки price'ov и avails'ov. Поскольку на 192 строке мы добавляем все имена товаров
            # на странице(18шт), а ниже мы проходим отдельно по каждому товару, то для дальшнейшего сопоставления
            # имени, цены, доступности я создаю отдельные списки, которые после окончание цикла extend'ят списки
            # prices, avails в общие списки products_price, products_available. Списки стираются при переходе на
            # следующюю страницу.
            prices = []
            avails = []

            # Проходим по каждому товару
            for ind, pid in enumerate(products_ids):

                # Создаем data-строку необходимую для post-запроса
                data_price = f'data={{"type":"product-buy","containers":' \
                             f'[{{"id":"{str(pid[0].get("id"))}","data":{{"id":"{str(pid[1].get("data-product"))}"}}}}]}}'
                data_avail = f'data={{"type":"avails","containers":' \
                             f'[{{"id":"{str(pid[0].get("id"))}","data":{{"id":"{str(pid[1].get("data-product"))}", "type":0,"useNotInStock":true}}}}]}}'

                # Выполняем цикл который:
                # 1) выполняет повторный запрос, при возникновении ошибки,
                # 2) добавляет в списки prices, avails - цену и доступность, которую получаем из response
                # post-запроса в JSON
                while True:

                    # Делаем запрос
                    response_price = session.post(config_dns.url_price_dns,
                                                  cookies=config_dns.cookies1_dns, headers=config_dns.headers1_dns,
                                                  data=data_price,
                                                  params=config_dns.params_dns)
                    response_avail = session.post(config_dns.url_avail_dns,
                                                  params=config_dns.params_dns,
                                                  cookies=config_dns.cookies1_dns,
                                                  headers=config_dns.headers1_dns, data=data_avail)

                    # Выполняется условие: если reponse 200, то добавляем результат в список и выходим из цикла, иначе
                    # если в response ошибка, то выполняем этоn же запрос повторно, пока не получим результат.
                    if response_price.ok and response_avail.ok:

                        # Явно достаем цену и доступность из JSON по ключам.
                        current = response_price.json()['data']['states'][0]['data']['price']['current']
                        avail = response_avail.json()['data']['states'][0]['data']['html']
                        avails.append(avail)
                        prices.append(current)
                        break
                    else:
                        continue
            products_price.extend(prices)
            products_available.extend(avails)

        # Создаем счетчик товаров
        product_count = 0

        # Группируем списки
        products_list = list(zip(products_name, products_price, products_available))

        # Создаем словарь в который добавляем полученные товары
        for prod in products_list:
            product_count += 1
            # Avail необходимо распарсить, поскольку из JSON'a достается HTML-разметка, а не текст...
            avail_soup = BeautifulSoup(prod[2], 'lxml')
            avail_res = avail_soup.text
            product_result_dns[product_count] = {
                'product_name': prod[0].text,
                'product_link': f"https://www.dns-shop.ru{prod[0].get('href')}",
                'product_price': prod[1],
                'product_available': True,  # пока что временно
            }

    # Делаем запись в БД
    # return save_db(product_result_dns, 'DNS')

    return product_result_dns


def main():
    scraper_dns()


if __name__ == '__main__':
    main()
