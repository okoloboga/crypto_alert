from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON

"""Создание и редактирование заданий"""
# Создание кнопок
new_task_button = InlineKeyboardButton(text=LEXICON['new_task'],
                                       callback_data='new_task')
view_task_button = InlineKeyboardButton(text=LEXICON['view_tasks'],
                                        callback_data='view_tasks')
# Соединение их в клавиатуру
main_keyboard = [[new_task_button], [view_task_button]]
# Объект клавиатуры
main_inline = InlineKeyboardMarkup(inline_keyboard=main_keyboard)

"""Выбор валютной пары"""
# Создание кнопок
eth_usd_button = InlineKeyboardButton(text=LEXICON['eth'],
                                      callback_data='eth')
btc_usd_button = InlineKeyboardButton(text=LEXICON['btc'],
                                      callback_data='btc')
cancel_button = InlineKeyboardButton(text="Отменить",
                                     callback_data='cancel')
# Соединение их в клавиатуру
pair_keyboard = [[eth_usd_button], [btc_usd_button], [cancel_button]]
# Объект клавиатуры
pair_inline = InlineKeyboardMarkup(inline_keyboard=pair_keyboard)

"""Выбор типа сигнала - ниже/выше чем"""
# Создание кнопок
up_button = InlineKeyboardButton(text=str('👆' + LEXICON['up'].capitalize() + '👆'),
                                 callback_data='up')
down_button = InlineKeyboardButton(text=('👇' + LEXICON['down'].capitalize() + '👇'),
                                   callback_data='down')
# Соединение их в клавиатуру
up_down_keyboard = [[up_button], [down_button], [cancel_button]]
# Объект клавиатуры
up_down_inline = InlineKeyboardMarkup(inline_keyboard=up_down_keyboard)

"""Ввод суммы"""

digit_keyboard = []

for j in range(3):
    digit_keyboard.append(
        [InlineKeyboardButton(text=str(i + j * 3 + 1), callback_data=str(i + j * 3 + 1)) for i in range(3)])

digit_keyboard.append([InlineKeyboardButton(text='<', callback_data='<'),
                       InlineKeyboardButton(text='0', callback_data='0'),
                       InlineKeyboardButton(text='ok', callback_data='ok')])
digit_keyboard.append([cancel_button])

digit_inline = InlineKeyboardMarkup(inline_keyboard=digit_keyboard)

"""Список задач"""


# На вход принимает список всех задач пользователя
def create_tasks_keyboard(*args: list) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    # Кнопки с задачами
    for button in args:
        kb_builder.row(InlineKeyboardButton(
            text=f"{button[0].upper()} {LEXICON[button[1]]} {button[2]}",
            callback_data=str(button)
        ))
    # Кнопка отмены
    kb_builder.row(
        InlineKeyboardButton(
            text='Отменить',
            callback_data='cancel'
        )
    )

    return kb_builder.as_markup()
