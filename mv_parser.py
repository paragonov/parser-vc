import requests
from configs_shops import config_mv
import math

products_result_mv = {}


def get_products_dict(session_mv, page, product_num):
    '''
    Функия предназначена для соеденения продуктов с их ценами и создания dict c продуктами.
    '''

    # Получаем кол-во offset на текущей странице
    offset = f'{page * 24}'
    config_mv.params_mv['offset'] = offset

    # Создаем dict c продуктами и их ценами
    items_prices = {}
    product_prices = get_products_prices(session_mv)
    for item in product_prices:
        item_id = item.get('price').get('productId')
        item_price = item.get('price').get('basePrice')

        items_prices[item_id] = {
            'item_price': item_price
        }

    # Получаем dict нужных нам продуктов
    product_list = get_products_list(session_mv)
    for product in product_list:
        product_id = product.get('productId')
        if product_id in items_prices:
            product_num += 1
            product_price = items_prices[product_id]
            products_result_mv[product_num] = {
                'product_name': product.get('name'),
                'product_link': f"https://www.mvideo.ru/products/{product.get('nameTranslit')}-{product_id}",
                'product_price': product_price.get('item_price'),
                'product_available': 1
            }


def get_products_prices(session_mv) -> dict:
    '''
    Функия предназначена для выполнения запросов и получения цен продуктов на текущей странице
    '''

    # Делаем запрос для получения id всех продуктов на текущей странице
    url_id = 'https://www.mvideo.ru/bff/products/listing'
    response = session_mv.get(url=url_id, params=config_mv.params_mv,
                              cookies=config_mv.cookies_mv, headers=config_mv.headers_mv)
    response = response.json()
    products_id = response.get('body').get('products')

    # Подставляем id продуктов в param для оформления post запроса
    config_mv.json_data_mv['productIds'] = products_id

    # Подставляем и переводим id продуктов в str в param_prices для получения prices
    products_id_str = ','.join(products_id)
    params_prices = {
        'productIds': products_id_str,
        'addBonusRubles': 'true',
        'isPromoApplied': 'true',
    }

    # Делаем запрос для получения prices всех продуктов на текущей странице
    url_prices = 'https://www.mvideo.ru/bff/products/prices'
    response_products_prices = session_mv.get(url=url_prices, params=params_prices,
                                              cookies=config_mv.cookies_mv,
                                              headers=config_mv.headers_mv)
    response_products_prices = response_products_prices.json()
    return response_products_prices.get('body').get('materialPrices')


def get_products_list(session_mv) -> dict:
    '''
    Функия предназначена для выполнения запроса и получения всех продуктов на текущей странице
    '''
    url_lists = 'https://www.mvideo.ru/bff/product-details/list'
    response_products_list = session_mv.post(url=url_lists,
                                             cookies=config_mv.cookies_mv,
                                             headers=config_mv.headers_mv, json=config_mv.json_data_mv)
    response_products_list = response_products_list.json()
    return response_products_list.get('body').get('products')


def get_pages_count(session_mv) -> int:
    '''
    Функция предназначена для получения количества страниц пагинации
    '''

    url_pages = 'https://www.mvideo.ru/bff/products/listing'
    response_pages = session_mv.get(url=url_pages, params=config_mv.params_mv,
                                    cookies=config_mv.cookies_mv, headers=config_mv.headers_mv)
    response_pages = response_pages.json()
    total_items_pages = response_pages.get('body').get('total')
    pages_count = math.ceil(total_items_pages / 24)
    return pages_count


def get_data_mv():
    '''
    Функция предназначена для создания сессии и запуска парсера сайта mvideo.ru
    '''
    product_num = 0

    # Создаем сессию
    with requests.Session() as session_mv:
        pages = get_pages_count(session_mv)

        # Проходим по полученным страницам
        for page in range(pages):
            get_products_dict(session_mv, page, product_num)
    return products_result_mv


def main():
    get_data_mv()


if __name__ == '__main__':
    main()
