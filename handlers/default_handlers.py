from copy import deepcopy
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from database.database import users_db, new_user
from keyboards.base_kb import main_inline

router = Router()


# Обработка команды СТАРТ вне состояний
@router.message(CommandStart())
async def process_start_command(message: Message):
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(new_user)

    await message.answer(text='Создать новое задание\n'
                              'просматривать и удалять\n'
                              'существующие задания',
                         reply_markup=main_inline)


# Обработка /cancel вне состояний
@router.callback_query(F.data == 'cancel', StateFilter(default_state))
async def process_cancel_command(callback: CallbackQuery):
    try:
        await callback.message.edit_text(text='Создать новое задание\n'
                                              'просматривать и удалять\n'
                                              'существующие задания',
                                         reply_markup=main_inline)
    except TelegramBadRequest:
        await callback.answer()


# Обработка /cancel в состояниях
@router.callback_query(F.data == 'cancel', ~StateFilter(default_state))
async def process_cancel_command(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(text='Создать новое задание\n'
                                              'просматривать и удалять\n'
                                              'существующие задания',
                                         reply_markup=main_inline)
        await state.clear()
    except TelegramBadRequest:
        await callback.answer()
