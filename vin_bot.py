import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
# import os
from aiogram.dispatcher.filters import Text
import json
from main1 import collect_data_magnit
from main2 import collect_data_diksy


bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async  def start(message: types.Message):
    start_buttons = ['Magnit', 'Diksi', 'K&B']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Товары со скидкой', reply_markup=keyboard)

@dp.message_handler(Text(equals="Magnit"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Please waiting...")

    collect_data_magnit()

    with open('Ярославль_magnit.json', encoding='utf-8') as f:
        data = json.load(f)

        for item in data:
            card = f"{hlink(item.get('Продукты'), item.get('Ссылка'))}\n" \
                f"{hbold('Прайс: ')} {item.get('Старая цена')}\n" \
                f"{hbold('Прайс со скидкой: ')} {item.get('Процент скидки')}: {item.get('Новая цена')}\n" \
                f"{hbold('Время акции: ')} {item.get('Время акции')}"

            await message.answer(card)


@dp.message_handler(Text(equals="Diksi"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Please waiting...")

    collect_data_diksy()

    with open('Ярославская область_diksy.json', encoding='utf-8') as f:
        data = json.load(f)

        for item in data:
            card = f"{hbold('Продукты: ')} {item.get('Продукты')}\n" \
                   f"{hbold('Прайс: ')} {item.get('Старая цена')}\n" \
                   f"{hbold('Прайс со скидкой: ')} {item.get('Процент скидки')}: {item.get('Новая цена')}\n" \
                   f"{hbold('Время акции: ')} {item.get('Время акции')}"

            await message.answer(card)


def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()

