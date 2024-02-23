from copy import deepcopy
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from database.database import users_db
from keyboards.base_kb import (main_inline, pair_inline,
                               up_down_inline, digit_inline)
from states.states import FSMMain

router = Router()


# Нажатие кнопки Новое задание и предоставление кнопок валют
@router.callback_query(F.data == 'new_task', StateFilter(default_state))
async def process_new_task_button(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(text='Выбери валюту для отслеживания\n'
                                              'ее стоимости к $\n\n',
                                         reply_markup=pair_inline)
        await callback.answer()
        await state.set_state(FSMMain.pair_choice)
    except TelegramBadRequest:
        await callback.answer()


# Выбор валют сделан - выбор нижнего/верхнего предела
@router.callback_query((F.data.in_(['btc', 'eth'])),
                       StateFilter(FSMMain.pair_choice))
async def process_pair_button(callback: CallbackQuery, state: FSMContext):
    try:
        await state.update_data(name=callback.data)
        await callback.message.edit_text(text='Выбери тип ценового предела\n'
                                              'Верхний или нижний\n\n',
                                         reply_markup=up_down_inline)
        await callback.answer()
        await state.set_state(FSMMain.up_down_choice)
    except TelegramBadRequest:
        await callback.answer()


# Неверный выбор валюты
@router.callback_query(StateFilter(FSMMain.pair_choice))
async def wrong_pair_command(callback: CallbackQuery):
    try:
        await callback.message.edit_text(text='Ты ввел что-то неверное...\n'
                                              'Выбери валюту для отслеживания\n'
                                              'ее стоимости к $\n\n',
                                         reply_markup=pair_inline)
        await callback.answer()
    except TelegramBadRequest:
        await callback.answer()


# Обработка нажатия кнопки с валютной парой и переход в следующее состояние
@router.callback_query((F.data.in_(['up', 'down'])),
                       StateFilter(FSMMain.up_down_choice))
async def process_pair_choice_button(callback: CallbackQuery, state: FSMContext):
    try:
        await state.update_data(up_down=callback.data)
        await state.update_data(price='')
        await callback.message.edit_text(text='Введи цену в $ для\n'
                                              'срабатывания сигнала\n\n',
                                         reply_markup=digit_inline)
        await callback.answer()
        await state.set_state(FSMMain.price_choice)
    except TelegramBadRequest:
        await callback.answer()


# Обработка ввода цены через клавиатуру
@router.callback_query((F.data.in_(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])),
                       StateFilter(FSMMain.price_choice))
async def process_pair_choice_button(callback: CallbackQuery, state: FSMContext):
    try:
        await state.update_data(price=str((await state.get_data())['price'] + callback.data))
        await callback.message.edit_text(text='Введи цену в $ для\n'
                                              'срабатывания сигнала\n\n'
                                              f"{str((await state.get_data())['price'])}\n\n",
                                         reply_markup=digit_inline)
        await callback.answer()
        await state.set_state(FSMMain.price_choice)
    except TelegramBadRequest:
        await callback.answer()


# Удаление или подтверждение цены ввода цены
@router.callback_query((F.data.in_(['<'])),
                       StateFilter(FSMMain.price_choice))
async def process_pair_choice_button(callback: CallbackQuery, state: FSMContext):
    if callback.data == '<':
        try:
            await state.update_data(price=str((await state.get_data())['price'][:-1]))
            await callback.message.edit_text(text='Введи цену в $ для\n'
                                                  'срабатывания сигнала\n\n'
                                                  f"{str((await state.get_data())['price'])}\n\n",
                                             reply_markup=digit_inline)
            await callback.answer()
            await state.set_state(FSMMain.price_choice)
        except TelegramBadRequest:
            await callback.answer()


# Неверный выбор предела
@router.callback_query(StateFilter(FSMMain.up_down_choice))
async def wrong_pair_command(callback: CallbackQuery):
    try:
        await callback.message.edit_text(text='Ты ввел что-то неверное...\n'
                                              'Выбери тип ценового предела\n'
                                              'Верхний или нижний\n\n',
                                         reply_markup=up_down_inline)
        await callback.answer()
    except TelegramBadRequest:
        await callback.answer()


# Обработка выбора цены
@router.callback_query(F.data == 'ok', StateFilter(FSMMain.price_choice))
async def process_price_command(callback: CallbackQuery, state: FSMContext):
    name = deepcopy((await state.get_data())['name'])
    up_down = deepcopy((await state.get_data())['up_down'])
    price = deepcopy((await state.get_data())['price'])

    users_db[callback.from_user.id].append([name, up_down, price])
    try:
        await callback.message.edit_text(text='Отлично! Задание сохранено\n'
                                              'его можно посмотреть или удалить\n\n'
                                              'При достижении указанного предела\n'
                                              'уведомления будут приходить раз в 1 минуту',
                                         reply_markup=main_inline)
        await callback.answer()
        await state.clear()
    except TelegramBadRequest:
        await callback.answer()


# Обработка неверного выбора цены
@router.callback_query(StateFilter(FSMMain.price_choice))
async def warning_price_command(callback: CallbackQuery):
    try:
        await callback.message.edit_text(text='Ты ввел что-то неверное...\n'
                                              'Введи цену в $ для\n'
                                              'срабатывания сигнала\n\n',
                                         reply_markup=digit_inline)
    except TelegramBadRequest:
        await callback.answer()
