import asyncio
import logging

from aiogram import Bot

from config_reader import config
from handler import dp as dispatcher


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())

dp = dispatcher


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())