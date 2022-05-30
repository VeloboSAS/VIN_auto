import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
# import os
from aiogram.dispatcher.filters import Text
import json
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from main import get_vin
from main import get_info_gos_uslugi
from main import get_info_gibdd


class DataInput(StatesGroup):
    num = State()


bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['VIN', 'Gibdd', 'Gosuslugi']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выбери услугу', reply_markup=keyboard)


@dp.message_handler(Text(equals="VIN"))
async def get_vin1(message: types.Message):
    await message.answer("Please waiting...")
    # await message.answer("Enter the car number: ")

    get_vin()

    await message.answer("Enter the car number: ")

# @dp.message_handler(Text(equals="VIN"))
# async def hello(message: types.Message):
#     await bot.send_message(message.from_user.id, 'Enter the car number: ')
#     await DataInput.num.set()
#
#
# @dp.message_handler(state=DataInput.num)
# async def get_vin1(message: types.Message, state: FSMContext):
#     num = message.text
#     vin = get_vin(num)
#     await message.answer(f"VIN:" + str(vin))
#     await state.finish()


@dp.message_handler(Text(equals="Diksi"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Please waiting...")

    get_info_gos_uslugi()

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

