import base64
import datetime

import otpauth
from aiogram import F
from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardRemove, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config_reader import config



SECRET = key = base64.b32decode(config.secret.get_secret_value(), casefold=True)
TOTP = otpauth.TOTP(
    secret=SECRET,
    digit=config.digit,
    period=config.period
)
dp = Dispatcher()



@dp.callback_query(lambda c: c.data == "update_code")
async def update_code(callback_query: types.CallbackQuery):
    time_live = datetime.datetime.now().timestamp()
    kb_update_code = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Обновить", callback_data="update_code")],
    ])
    await callback_query.message.edit_text(
        f"Текущий код: {TOTP.generate():06}, срок жизни: {time_live % 30 :.2f} / 30",
        reply_markup=kb_update_code
    )
    await callback_query.answer()


@dp.message(Command('get_code'))
async def get_code(msg: Message):
    cmd = msg.text.split()
    if not ((msg.from_user.id == config.tg_admin_id) or len(cmd) >= 2 and cmd[
        1] == config.access_password.get_secret_value()):
        await msg.answer("Access denied!")
        return

    time_live = datetime.datetime.now().timestamp()

    kb_update_code = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Обновить", callback_data="update_code")],
    ])
    await msg.answer(f"Текущий код: {TOTP.generate():06}, срок жизни: {time_live % 30 :.2f} / 30",
                     reply_markup=kb_update_code
    )


@dp.message(Command('get_cred'))
async def get_credentials(msg: Message):
    cmd = msg.text.split()
    if not ((msg.from_user.id == config.tg_admin_id) or len(cmd) >= 2 and cmd[1] == config.access_password.get_secret_value()):
        await msg.answer("Access denied!")
        return

    await msg.answer(f"login: {config.login}, password: {config.password.get_secret_value()}\n")

