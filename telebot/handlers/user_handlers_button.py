from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from telebot.keyboards.keyboards import create_store_list_keyboard
from telebot.lexicon.lexicon_ru import LEXICON_RU
import sqlite3

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
async def process_about_me_command(message: Message):
    await message.answer(LEXICON_RU[message.text], reply_markup=create_store_list_keyboard())







# # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# # "Обо мне" в главном меню показывает сообщение и кнопку "назад"
# @router.callback_query(F.data == '/about_me')
# async def process_about_me(callback: CallbackQuery):
#     await callback.message.edit_text(text=LEXICON_RU['/about_me'], reply_markup=create_back_keyboard('/start'))
#     await callback.answer()
#
# # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# # "Наша почта" в меню "Поддержка" выводить почту и кнопку "назад"
# @router.callback_query(F.data == 'email')
# async def process_email(callback: CallbackQuery):
#     await callback.message.edit_text(
#         text=LEXICON_RU['email_send'], reply_markup=create_back_keyboard('/help'))
#     await callback.answer()
