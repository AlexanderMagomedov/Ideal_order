from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async
from django.db import IntegrityError
import sqlite3
from telebot.filters.filters import IsStore, IsMassa, DeleteOrder
from telebot.keyboards.keyboards import create_store_list_keyboard, create_massa_keyboard, create_orders_list_keyboard
from telebot.lexicon.lexicon_ru import LEXICON_RU


from telebot.models import Order, Store, User

router = Router()


# Функция фильтр если пользователь сотрудник
def filter_is_not_staff(message: Message):
    return str(message.from_user.id) not in give_all_telegram_id()


# Этот хендлер срабатывает если пользователь не сотрудник
@router.message(filter_is_not_staff)
async def process_start_command(message: Message):
        await message.answer(f'{LEXICON_RU["/start_bad"]} {message.from_user.id}')


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
    try:
        await add_order(callback.data)
        await callback.message.edit_text(text=LEXICON_RU['order_success'], reply_markup=create_store_list_keyboard())
        await callback.answer()
    except User.DoesNotExist:
        await callback.message.edit_text(text=LEXICON_RU['order_bad'])
        await callback.answer()
    except IntegrityError:
        await callback.message.edit_text(text=LEXICON_RU['order_exist'], reply_markup=create_store_list_keyboard())
        await callback.answer()


@sync_to_async
def add_order(callback: str):
    order = Order(
        store=Store.objects.get(store_name=' '.join(callback.split()[2:])),
        user=User.objects.get(telegram_id=callback.split()[0]),
        massa=callback.split()[1]
    )
    order.save()


# Этот хэндлер будет срабатывать на команду "/orders"
# и отправлять пользователю список инлайн кнопок с названиями магазинов и
@router.message(Command(commands='orders'))
async def process_store_list_command(message: Message):
    if give_all_orders():
        await message.answer(LEXICON_RU[message.text], reply_markup=create_orders_list_keyboard(give_all_orders()))
    else:
        await message.answer(LEXICON_RU['no_orders'])


# Функция возвращает полный список всех заявок
def give_all_orders():
    connect = sqlite3.connect('db.sqlite3')
    cursor = connect.cursor()
    orders = (list(map(lambda x: x[0], cursor.execute("SELECT store_name FROM telebot_order JOIN telebot_store ON telebot_store.id = telebot_order.store_id").fetchall())))
    connect.close()
    return orders


@router.callback_query(DeleteOrder())
async def process_delete_order_press(callback: CallbackQuery):
    await delete_order(callback)
    await callback.message.edit_text(
        text=LEXICON_RU['delete_success'],
        reply_markup=create_orders_list_keyboard(give_all_orders()))
    await callback.answer()

@sync_to_async
def delete_order(callback):
    order = Order.objects.filter(store_id=Store.objects.get(store_name=' '.join(callback.data.split()[1:])).id)
    order.delete()
