import asyncio
from aiogram import types, Dispatcher, Bot
from aiogram.filters import Command

bot_token = "8402527695:AAFodxLP6Kq-R2jPwyAF00NUxe9PcPj6PjA"

bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(Command("start"))
async def command_start(message: types.Message):
    await message.answer("hey")

@dp.message(Command("help"))
async def command_help(message: types.Message):
    await message.answer("I don`t help you 🤣🤣🤣")   


@dp.message(Command("o"))
async def command_(message: types.Message):
    await message.answer_dice(emoji="🎳")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())    