import base64
import datetime
import json

import otpauth
from aiogram import Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from config_reader import config


with open('data.json', encoding="UTF-8") as f:
    data: dict = json.load(f)

if not data:
    raise ValueError("not founded data.json")


totp: dict[int, list] = {}

for k, v in data.items():
    totp_data = v.get("totp")

    access_list = v.get("access_list")
    secret = base64.b32decode(totp_data.get('secret'), casefold=True)

    totp[int(k)] = [
        otpauth.TOTP(
            secret=secret,
            digit=totp_data.get('digit'),
            period=totp_data.get('period')
        ),
        access_list,
        [v.get("login"), v.get("password")],
        v.get('alies')
    ]


dp = Dispatcher()

chat_id = None
message_id = None

@dp.message(Command('start'))
async def get_message(msg: types.Message):
    print(f"chat_id: {msg.chat.id}")

    print("message_id: ", (await msg.answer("init_message")).message_id)






