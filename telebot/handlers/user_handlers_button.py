from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async

from telebot.filters.filters import IsStore, IsMassa
from telebot.keyboards.keyboards import create_store_list_keyboard, create_massa_keyboard
from telebot.lexicon.lexicon_ru import LEXICON_RU
import sqlite3

from telebot.models import Order, Store, User

router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    if telegram_id_exist(message):
        await message.answer(LEXICON_RU['/start_good'])
    else:
        await message.answer(f'{LEXICON_RU["/start_bad"]} {message.from_user.id}')


# Проверяет что пользователь есть в списке сотрудников
def telegram_id_exist(message) -> bool:
    if str(message.from_user.id) in give_all_telegram_id():
        return True


# Функция возвращает полный список всех телеграм ид сотрудников
def give_all_telegram_id():
    connect = sqlite3.connect('db.sqlite3')
    cursor = connect.cursor()
    user_list_all = (list(map(lambda x: x[0], cursor.execute("SELECT telegram_id FROM telebot_user").fetchall())))
    connect.close()
    return user_list_all


# Этот хэндлер будет срабатывать на команду "/store_list"
# и отправлять пользователю список инлайн кнопок с названиями магазинов
@router.message(Command(commands='store_list'))
async def process_store_list_command(message: Message):
    await message.answer(LEXICON_RU[message.text], reply_markup=create_store_list_keyboard())


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# в списке доступных сказок Запускать первую страницу сказки
@router.callback_query(IsStore())
async def process_create_order_press(callback: Message):
    await callback.message.edit_text(
        text=LEXICON_RU['massa'], reply_markup=create_massa_keyboard(callback.data, callback.from_user.id))


@router.callback_query(IsMassa())
async def process_save_order_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['order_success'])
    await add_order(callback.data)
    await callback.answer()


@sync_to_async
def add_order(callback: str):
    order = Order(
        store=Store.objects.get(store_name=callback.split()[0]),
        user=User.objects.get(telegram_id=callback.split()[1]),
        massa=callback.split()[2]
    )
    order.save()

