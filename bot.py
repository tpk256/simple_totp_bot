import asyncio
import logging
import base64
import datetime
import json

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
import otpauth

from config_reader import config


with open('data.json', encoding="UTF-8") as f:
    data: dict = json.load(f)

if not data:
    raise ValueError("not founded data.json")


totp: dict[int, list] = {}

users = []

for k, v in data.items():
    totp_data = v.get("totp")
    secret = base64.b32decode(totp_data.get('secret'), casefold=True)
    users.append([otpauth.TOTP(
            secret=secret,
            digit=totp_data.get('digit'),
            period=totp_data.get('period')
        ), v.get('alies')])



logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())



chat_id = config.chat_id
message_id = config.message_id





async def main():

    interval = 4.3
    while True:
        try:
            time_live = datetime.datetime.now().timestamp()
            dt = datetime.datetime.fromtimestamp(int(time_live))

            await bot.edit_message_text(
                text=
                f"Актуальные коды кичена #code\n"
                f"УЗ: {users[0][1]}\n"
                f"Текущий код: {users[0][0].generate():06}, срок жизни: {time_live % 30 :.2f} / 30\n"
                f"Дата и время последнего обновления: {dt}\n"
                f"УЗ: {users[1][1]}\n"
                f"Текущий код: {users[1][0].generate():06}, срок жизни: {time_live % 30 :.2f} / 30\n"
                f"Дата и время последнего обновления: {dt}"

                ,
                chat_id=chat_id,
                message_id=message_id
            )
            await asyncio.sleep(interval)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await bot.send_message(
                chat_id=config.tg_admin_id,
                text="был флуд"
            )
        except Exception as e:
            await bot.send_message(
                chat_id=config.tg_admin_id,
                text=f"Неизвестная ошибка {e}"
            )




if __name__ == "__main__":
    asyncio.run(main())