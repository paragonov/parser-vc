import time

import telebot
from telebot import types
from telebot.formatting import hlink, hbold

from cl_parser import get_data_cl
# from cu_parser import get_data_cu
from dns_parser import scraper_dns
from mv_parser import get_data_mv

bot = telebot.TeleBot('5499460518:AAFCtWIXEOu34Z2doRuefKOHy_raRr_YNzE', parse_mode='HTML')


@bot.message_handler(commands=['start'])
def start_bot(message: types.Message):
    start_buttons = ['Мвидео', 'DNS', 'Ситилинк', 'ComputerUniverse', ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    bot.send_message(message.chat.id, text='Выберите магазин', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_data_vc(message: types.Message):
    data = {}
    if message.text == 'DNS':
        bot.send_message(chat_id=message.chat.id, text='Идет сбор информации... \n'
                                                       'Это может занять какое-то время...')
        data = scraper_dns()
    elif message.text == 'Мвидео':
        bot.send_message(chat_id=message.chat.id, text='Идет сбор информации... \n')
        data = get_data_mv()
    elif message.text == 'Ситилинк':
        bot.send_message(chat_id=message.chat.id, text='Идет сбор информации... \n')
        data = get_data_cl()
    elif message.text == 'ComputerUniverse':
        bot.send_message(chat_id=message.chat.id, text='Идет сбор информации... \n'
                                                       'Это может занять какое-то время...')
        # data = handling_func(get_data_cu, message)
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Такого магазина нет в отработке... \n Выберете другой магазин...')

    if data:
        for ind, item in enumerate(data.values()):
            prod = get_data(item)
            bot.send_message(chat_id=message.chat.id, text=prod)
            if ind % 10 == 0:
                time.sleep(2)
    else:
        bot.send_message(chat_id=message.chat.id, text='Упс... Произошла ошибка. \n'
                                                       'Попробуйте снова.')
    bot.send_message(chat_id=message.chat.id, text='Выберите следующий магазин...')


def get_data(item):
    '''Функция предназначеня для обработки входных данных с парсера на вывод в чат'''

    return f'{hlink(item.get("product_name"), item.get("product_link"))}\n' \
           f'{hbold("Цена: ")}{item.get("product_price")}\n' \
           f'{hbold("В наличии: ")}{"Да" if item.get("product_available") else "Нет в наличии"}'


def handling_func(func, message):
    '''Декоратор для проверки функции на ошибки'''

    def wrapper():
        try:
            result = func()
        except LookupError:
            bot.send_message(chat_id=message.chat.id, text='Упс... Произошла ошибка. \n'
                                                           'Попробуйте снова.')
        else:
            return result

    return wrapper()


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
