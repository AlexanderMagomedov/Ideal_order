from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sqlite3


# Функция создания инлайн кнопкок со списком магазинов
def create_store_list_keyboard() -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками
    kb_builder.row(*[InlineKeyboardButton(
        text=story_name,
        callback_data=story_name) for story_name in give_all_store()], width=1)
    return kb_builder.as_markup()


# Функция возвращает полный список всех телеграм ид сотрудников
def give_all_store():
    connect = sqlite3.connect('db.sqlite3')
    cursor = connect.cursor()
    store_list = (list(map(lambda x: x[0], cursor.execute("SELECT store_name FROM telebot_store").fetchall())))
    connect.close()
    return store_list


# Функция создания инлайн кнопок с
def create_massa_keyboard(store_name, telegram_id) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками
    kb_builder.row(*[InlineKeyboardButton(
        text=f'{i} кг',
        callback_data=f'{telegram_id} {i} {store_name}') for i in range(2, 32)], width=5)
    return kb_builder.as_markup()


# Функция создания инлайн кнопкок с заявками
def create_orders_list_keyboard(arg) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками
    for story_name in arg:
        kb_builder.row(InlineKeyboardButton(
            text=f'Закрыть заявку по {story_name}',
            callback_data=f'delete {story_name}'))
    return kb_builder.as_markup()


# # Функция создания инлайн кнопки "Назад" в главном меню
# def create_back_keyboard(arg) -> InlineKeyboardMarkup:
#     # Создаем объект клавиатуры
#     kb_builder = InlineKeyboardBuilder()
#     # Наполняем клавиатуру кнопками-закладками в порядке возрастания
#     kb_builder.row(InlineKeyboardButton(
#         text=LEXICON_RU['back'],
#         callback_data=arg))
#     return kb_builder.as_markup()
#
#
# # Функция создания инлайн кнопкок со списком сказок
# def create_story_list_keyboard(page) -> InlineKeyboardMarkup:
#     # Создаем объект клавиатуры
#     kb_builder = InlineKeyboardBuilder()
#     # Наполняем клавиатуру кнопками-закладками
#     kb_builder.row(*[InlineKeyboardButton(
#         text=story_name,
#         callback_data=story_name) for story_name in page_list()[page]], width=1)
#     kb_builder.row(*[InlineKeyboardButton(
#         text=text,
#         callback_data=comand)
#         for text, comand in ((LEXICON_RU['backward'], (f'backward {page}')), (LEXICON_RU['forward'], (f'forward {page}')))], width=2)
#     kb_builder.row(InlineKeyboardButton(
#         text=LEXICON_RU['back'],
#         callback_data='/start'))
#     return kb_builder.as_markup()
#
#
# def create_story_keyboard(page, book_name) -> InlineKeyboardMarkup:
#     # Создаем объект клавиатуры
#     kb_builder = InlineKeyboardBuilder()
#     # Наполняем клавиатуру кнопками-закладками
#     kb_builder.row(*[InlineKeyboardButton(
#         text=text,
#         callback_data=comand)
#         for text, comand in ((LEXICON_RU['backward'],
#                               (f'bstory {page} {book_name}')),
#                              (LEXICON_RU['forward'],
#                               (f'fstory {page} {book_name}')))], width=2)
#     kb_builder.row(InlineKeyboardButton(
#         text=LEXICON_RU['back'],
#         callback_data='/read'))
#     return kb_builder.as_markup()
