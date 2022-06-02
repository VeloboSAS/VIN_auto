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
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['VIN', 'Gibdd', 'Gosuslugi']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выбери услугу', reply_markup=keyboard)


@dp.message_handler(Text(equals="VIN"))
async def hello(message: types.Message):
    await bot.send_message(message.from_user.id, 'Enter the car number: ')
    await DataInput.num.set()


@dp.message_handler(state=DataInput.num)
async def get_vin1(message: types.Message, state: FSMContext):
    num = message.text
    vin = get_vin(num)
    await message.answer(str(vin))
    await state.finish()


@dp.message_handler(Text(equals="Gosuslugi"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Please waiting...")
    vin = "X9FMXXEEBMCG01011"
    get_info_gos_uslugi(vin)

    with open('data.json', encoding='utf-8') as f:
        data = json.load(f)

        for item in data:
            card = f"{hbold('Номер реестровой записи')} {item.get('Номер реестровой записи')}\n" \
                   f"{hbold('Статус в ГИБДД')} {item.get('Статус в ГИБДД')}\n" \
                   f"{hbold('Наименование подразделения')} {item.get('Наименование подразделения')}\n" \
                   f"{hbold('Последняя операция')} {item.get('Последняя операция')}\n" \
                   f"{hbold('В лизинге')} {item.get('В лизинге')}\n" \
                   f"{hbold('Марка и модель')} {item.get('Марка и модель')}\n" \
                   f"{hbold('Год выпуска')} {item.get('Год выпуска')}\n" \
                   f"{hbold('Изготовитель')} {item.get('Изготовитель')}\n" \
                   f"{hbold('Идентификационный номер (VIN)')} {item.get('Идентификационный номер (VIN)')}\n" \
                   f"{hbold('Идентификационный номер (VIN2)')} {item.get('Идентификационный номер (VIN2)')}\n" \
                   f"{hbold('Номер шасси (рамы)')} {item.get('Номер шасси (рамы)')}\n" \
                   f"{hbold('Номер кузова (кабины)')} {item.get('Номер кузова (кабины)')}\n" \
                   f"{hbold('Цвет кузова (кабины)')} {item.get('Цвет кузова (кабины)')}\n" \
                   f"{hbold('Рабочий объём (куб.см)')} {item.get('Рабочий объём (куб.см)')}\n" \
                   f"{hbold('Модель двигателя')} {item.get('Модель двигателя')}\n" \
                   f"{hbold('Тип топлива')} {item.get('Тип топлива')}\n" \
                   f"{hbold('Мощность (кВТ/л.с.)')} {item.get('Мощность (кВТ/л.с.)')}\n" \
                   f"{hbold('Тип транспортного средства')} {item.get('Тип транспортного средства')}\n" \
                   f"{hbold('Категория')} {item.get('Категория')}\n" \
                   f"{hbold('Категория (Там. Союз)')} {item.get('Категория (Там. Союз)')}\n" \
                   f"{hbold('Экологический класс')} {item.get('Экологический класс')}\n" \
                   f"{hbold('Положение руля')} {item.get('Положение руля')}\n" \
                   f"{hbold('Тип коробки передач')} {item.get('Тип коробки передач')}\n" \
                   f"{hbold('Тип привода')} {item.get('Тип привода')}\n" \
                   f"{hbold('Серия и номер одобрения типа')} {item.get('Серия и номер одобрения типа')}\n" \
                   f"{hbold('Статус утилизационного сбора')} {item.get('Статус утилизационного сбора')}\n" \
                   f"{hbold('Номер таможенной декларации (ТД, ТПО)')} {item.get('Номер таможенной декларации (ТД, ТПО)')}\n" \
                   f"{hbold('Таможенные ограничения')} {item.get('Таможенные ограничения')}\n" \
                   f"{hbold('История регистрационных действий')} {item.get('История регистрационных действий')}\n" \
                   f"{hbold('В розыске')} {item.get('В розыске')}\n" \
                   f"{hbold('Ограничения на регистрацию')} {item.get('Ограничения на регистрацию')}\n" \
                   f"{hbold('В розыске ПТС')} {item.get('В розыске ПТС')}\n"
                   # f"{hbold('Находится в залоге')} {item.get('Находится в залоге')}\n"

            await message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()

