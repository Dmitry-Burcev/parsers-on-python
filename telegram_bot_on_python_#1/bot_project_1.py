import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot_token = "8402527695:AAFodxLP6Kq-R2jPwyAF00NUxe9PcPj6PjA"

users = {}
is_waiting = False
user_name = None


bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global is_waiting
    is_waiting = True

    await message.answer("Hey!")
    await message.answer("What`s your name? Write on a keyboard.")


@dp.message()
async def handle_name(message: types.Message):
    global is_waiting, user_name
    if is_waiting:
        user_name = message.text
        if user_name not in users:
            users[user_name] = 100
        else:
            await message.answer("You already in system")

        await message.answer(f"Your name is {user_name} and balance is {users[user_name]}")
        is_waiting = False

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="add balance", callback_data="add_balance")]
            ]
        )

        await message.answer("Do you want to add balance?", reply_markup=keyboard)
    else:
        await message.answer("I don`t now this! Try another.")    


@dp.callback_query(lambda x: x.data == "add_balance")
async def callback_balance(callback: types.CallbackQuery):
    global user_name
    users[user_name] += 50

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="add balance again", callback_data="add_balance")]
        ]
    )

    await callback.message.edit_text(f"New balance {user_name} - {users[user_name]}", reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())