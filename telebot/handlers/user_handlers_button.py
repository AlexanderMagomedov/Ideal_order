import sqlite3

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async
from django.db import IntegrityError

from telebot.filters.filters import IsStore, IsMassa, give_all_telegram_id
from telebot.keyboards.keyboards import create_store_list_keyboard, create_massa_keyboard
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
        await callback.message.edit_text(text=LEXICON_RU['order_success'])
        await add_order(callback.data)
        await callback.answer()
    except User.DoesNotExist:
        await callback.message.edit_text(text=LEXICON_RU['order_bad'])
        await callback.answer()
    except IntegrityError:
        await callback.message.edit_text(text=LEXICON_RU['order_exist'])
        await callback.answer()


@sync_to_async
def add_order(callback: str):
    order = Order(
        store=Store.objects.get(store_name=callback.split()[0]),
        user=User.objects.get(telegram_id=callback.split()[1]),
        massa=callback.split()[2]
    )
    order.save()



