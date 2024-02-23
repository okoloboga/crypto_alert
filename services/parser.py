import time
import requests
import asyncio

from bs4 import BeautifulSoup
from database.database import users_db
from aiogram import Bot
from config_data.config import Config, load_config

# Загружаем конфиг в переменную config
config: Config = load_config()

# Инициализируем бот в диспетчере
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


def get_crypto_rank(coins: list) -> dict:
    result = {}
    html_resp = requests.get("https://coinranking.com/ru").text
    block = BeautifulSoup(html_resp, "lxml")
    rows = block.find_all("tr", class_="table__row--full-width")

    for row in rows:
        ticker = row.find("span", class_="profile__subtitle-name")
        if ticker:
            ticker = ticker.text.strip().lower()
            if ticker in coins:
                price = row.find("td", class_="table__cell--responsive")
                if price:
                    price = int(float(price.find("div", class_="valuta--light").text \
                                      .replace("$", "").replace(",", ".").replace(" ", "") \
                                      .replace("\n", "").replace("\xa0", "").replace(".", "")))
                result[ticker.lower()] = price // 100
    return result


async def price_alert(user_id: int, text: str):
    await bot.send_message(user_id, text)


# Если цена достигает цели, отправляем уведомление в телегу
def check_coins_balance(loop):
    while True:
        for user_id, tasks in users_db.items():
            if len(tasks) != 0:
                for task in tasks:
                    coin_dict = get_crypto_rank(task)

                    if task[0] in coin_dict:
                        if task[1] == 'up':
                            if int(coin_dict.get(task[0])) >= int(task[2]):
                                asyncio.set_event_loop(loop)
                                loop.run_until_complete(price_alert(user_id, f"[{task[0].upper()}] дороже\n"
                                                                                  f'{coin_dict.get(task[0])} $'))
                        if task[1] == 'down':
                            if int(coin_dict.get(task[0])) <= int(task[2]):
                                asyncio.set_event_loop(loop)
                                loop.run_until_complete(price_alert(user_id, f"[{task[0].upper()}] дешевле\n"
                                                                                  f'{coin_dict.get(task[0])} $'))

        time.sleep(20)
