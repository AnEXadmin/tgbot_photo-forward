import asyncio
import logging
from sys import stdout
from handlkeep import dp
from aiogram import executor
from config import root_id
from dbkeep import create_db, set_default_commands
from load_all import bot

async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    await create_db()
    await bot.send_message(root_id, "Бот включен!")
    await set_default_commands(bot)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=True)
