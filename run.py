import asyncio
from aiogram import Router, Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import logging

from configs import TOKEN
from handlers import admin_handlers
from handlers.admin_handlers import admin_router

dp = Dispatcher()
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.include_router(admin_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    asyncio.run(main())
