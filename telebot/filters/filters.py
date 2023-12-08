from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from telebot.keyboards.keyboards import give_all_store
import sqlite3


# Функция возвращает полный список всех телеграм ид сотрудников
def give_all_telegram_id():
    connect = sqlite3.connect('db.sqlite3')
    cursor = connect.cursor()
    user_list_all = (list(map(lambda x: x[0], cursor.execute("SELECT telegram_id FROM telebot_user").fetchall())))
    connect.close()
    return user_list_all


class IsStore(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data in give_all_store()


class IsMassa(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.split()[0] in give_all_store()
