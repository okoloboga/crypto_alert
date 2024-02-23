from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from database.database import users_db
from filters.filters import IsTask
from keyboards.base_kb import create_tasks_keyboard, main_inline

router = Router()


# Просмотр задания
@router.callback_query(F.data == 'view_tasks')
async def process_view_tasks_button(callback: CallbackQuery):
    if users_db[callback.from_user.id]:
        try:
            await callback.message.edit_text(text='Текущие задачи\n'
                                                  'Нажми на задачу, что бы\n'
                                                  'её удалить',
                                             reply_markup=create_tasks_keyboard(
                                                 *users_db[callback.from_user.id])
                                             )
        except TelegramBadRequest:
            await callback.answer()

        await callback.answer()
    else:
        try:
            await callback.message.edit_text(text='Нет задач',
                                             reply_markup=main_inline)
            await callback.answer()
        except TelegramBadRequest:
            await callback.answer()


# Процесс удаления задания
@router.callback_query(IsTask())
async def process_delete_task_button(callback: CallbackQuery):
    task = callback.data.replace("[", "").replace("]", "").replace("'", "").replace(",", "").split()
    users_db[callback.from_user.id].remove(task)

    if users_db[callback.from_user.id]:
        try:
            await callback.message.edit_text(text='Текущие задачи\n\n'
                                                  'Нажми на задачу, что бы\n'
                                                  'её удалить',
                                             reply_markup=create_tasks_keyboard(
                                                 *users_db[callback.from_user.id])
                                             )
            await callback.answer()
        except TelegramBadRequest:
            await callback.answer()
    else:
        try:
            await callback.message.edit_text(text='Нет задач',
                                             reply_markup=main_inline)
            await callback.answer()
        except TelegramBadRequest:
            await callback.answer()
