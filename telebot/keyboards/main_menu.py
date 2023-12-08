from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telebot.lexicon.lexicon_ru import LEXICON_COMMANDS


# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command,
        description in LEXICON_COMMANDS.items()]
    await bot.set_my_commands(main_menu_commands)


# Функция создания инлайн кнопок главного меню
def create_menu_keyboard() -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    kb_builder.row(
        InlineKeyboardButton(text=LEXICON_COMMANDS['/about_me'], callback_data='/about_me'),
        InlineKeyboardButton(text=LEXICON_COMMANDS['/help'], callback_data='/help'),
        InlineKeyboardButton(text=LEXICON_COMMANDS['/read'], callback_data='/read'), width=1
    )
    return kb_builder.as_markup()