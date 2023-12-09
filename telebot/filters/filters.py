from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from telebot.keyboards.keyboards import give_all_store


class IsStore(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data in give_all_store()


class IsMassa(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return ' '.join(callback.data.split()[2:]) in give_all_store()
