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

@dp.message(Command('start'))
async def start(msg: Message):
    user_id = msg.from_user.id
    access_list: list[int] = []

    for k, v in totp.items():
        if user_id in v[1]:
            access_list.append(k)


    if not access_list:
        await msg.answer("Access denied!")
        return


    inline_keyboard = []

    for id in access_list:
        inline_keyboard.append(
            InlineKeyboardButton(text=f"{totp[id][-1]} ", callback_data=f"data_{id}")
        )


    kb_data = InlineKeyboardMarkup(inline_keyboard=[inline_keyboard])
    await msg.answer(f"Доступные вам УЗ",
                     reply_markup=kb_data
    )



@dp.callback_query(lambda c: c.data.startswith("data_")  )
async def get_data(callback_query: types.CallbackQuery):
    id = int(callback_query.data.strip("data_"))

    time_live = datetime.datetime.now().timestamp()

    kb_update_code = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Обновить", callback_data=f"code_{id}")],
    ])


    totp_code, ac_list, cred, alies  = totp[id]

    if callback_query.from_user.id not in ac_list:
        await callback_query.message.edit_text("Access Denied")
        return await callback_query.answer("ACcess Denied!")

    await callback_query.message.edit_text(
        f"УЗ: {alies}\n"
        f"login: {cred[0]} \n"
        f"password: {cred[1]} \n"
        f"Текущий код: {totp_code.generate():06}, срок жизни: {time_live % 30 :.2f} / 30",
        reply_markup=kb_update_code
    )

    await callback_query.answer()



@dp.callback_query(lambda c: c.data.startswith("code_"))
async def update_code(callback_query: types.CallbackQuery):
    id = int(callback_query.data.strip("code_"))

    time_live = datetime.datetime.now().timestamp()

    kb_update_code = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Обновить", callback_data=f"code_{id}")],
    ])

    totp_code, ac_list, cred, alies = totp[id]

    if callback_query.from_user.id not in ac_list:
        await callback_query.message.edit_text("Access Denied")
        return await callback_query.answer("ACcess Denied!")

    await callback_query.message.edit_text(
        f"УЗ: {alies}\n"
        f"login: {cred[0]} \n"
        f"password: {cred[1]} \n"
        f"Текущий код: {totp_code.generate():06}, срок жизни: {time_live % 30 :.2f} / 30",
        reply_markup=kb_update_code
    )

    await callback_query.answer()

