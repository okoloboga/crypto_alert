from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from database.database import users_db


class IsTask(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        task = callback.data.replace("[", "").replace("]",
                                                      "").replace("'", "").replace(",", "").split()

        coins = ['btc', 'eth']
        up_down = ['up', 'down']

        return (task[0] in coins) and (task[1] in up_down) and task[2].isdigit()
