import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink

from dns_parser import get_data_dns
from mv_parser import get_data_mv
from cl_parser import get_data_cl
from cu_parser import get_data_cu

bot = Bot(token='TOKEN', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Мвидео', 'DNS', 'Ситилинк', 'ComputerUniverse', ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите магазин', reply_markup=keyboard)


@dp.message_handler(Text(equals='Мвидео'))
async def get_prod_mv(message: types.Message):
    await message.answer('Идет сбор информации... \n')
    chat_id = message.chat.id
    await send_data('Мвидео', chat_id)


@dp.message_handler(Text(equals='DNS'))
async def get_prod_dns(message: types.Message):
    await message.answer('Идет сбор информации... \n'
                         'Это может занять какое-то время...')
    chat_id = message.chat.id
    await send_data('DNS', chat_id)


@dp.message_handler(Text(equals='ComputerUniverse'))
async def get_prod_cu(message: types.Message):
    await message.answer('Идет сбор информации... \n'
                         'Это может занять какое-то время...')
    chat_id = message.chat.id
    await send_data('CU', chat_id)


@dp.message_handler(Text(equals='Ситилинк'))
async def get_prod_cl(message: types.Message):
    await message.answer('Идет сбор информации... \n')
    chat_id = message.chat.id
    await send_data('Ситилинк', chat_id)


async def send_data(shop, chat_id):
    data = None

    if shop == 'DNS':
        data = handling_func(get_data_dns)
    elif shop == 'Мвидео':
        data = handling_func(get_data_mv)
    elif shop == 'Ситилинк':
        data = handling_func(get_data_cl)
    elif shop == 'CU':
        data = handling_func(get_data_cu)
    else:
        await bot.send_message(chat_id=chat_id, text='Такого магазина нет в отработке... \n Выберете другой магазин...')

    if data:
        for ind, item in enumerate(data.values()):
            prod = await get_data(item)
            await bot.send_message(chat_id=chat_id, text=prod)
            if ind % 10 == 0:
                time.sleep(2)
        await bot.send_message(chat_id=chat_id, text='Выберите следующий магазин...')
    else:
        await bot.send_message(chat_id=chat_id, text='Упс... Произошла ошибка. \n'
                                               'Попробуйте снова.')


async def get_data(item):
    '''Функция предназначеня для обработки входных данных с парсера на вывод в чат'''

    return f'{hlink(item.get("product_name"), item.get("product_link"))}\n' \
           f'{hbold("Цена: ")}{item.get("product_price")}\n' \
           f'{hbold("В наличии: ")}{"Да" if item.get("product_available") else "Нет в наличии"}'


def handling_func(func):
    '''Декоратор для проверки функции на ошибки'''
    def wrapper():
        try:
            result = func()
        except Exception:
            print('s')
        else:
            return result
    return wrapper()


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
