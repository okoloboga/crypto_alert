from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_data.config import Config, load_config
from keyboards.main_menu import set_main_menu
from handlers import (new_task_handlers, other_handlers,
                      list_task_handlers, default_handlers)
from services.parser import check_coins_balance

import asyncio
import logging
import threading

loop = asyncio.new_event_loop()
threading.Thread(target=check_coins_balance, args=(loop,)).start()

# Инициализация логгера
logger = logging.getLogger(__name__)

# Инициализация хранилища
storage = MemoryStorage()


# Конфигурирование и запуск Бота
async def main():

    # Конфигурирование логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    
    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот в диспетчере
    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')
    dp = Dispatcher()

    # Настройка главного меню бота
    await set_main_menu(bot)

    # Регистрация роутеров в диспетчере
    dp.include_router(default_handlers.router)
    dp.include_router(new_task_handlers.router)
    dp.include_router(list_task_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запскаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    return bot

if __name__ == '__main__':
    asyncio.run(main())

