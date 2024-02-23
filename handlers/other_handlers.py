from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.exceptions import TelegramBadRequest

from keyboards.base_kb import main_inline

router = Router()


# Обработка любых сообщений не предусмотренных логикой бота
@router.callback_query(StateFilter(default_state))
async def send_echo(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.answer(text='Ты сказал что то непонятное',
                                      reply_markup=main_inline)
    except TelegramBadRequest:
        await callback.answer()
