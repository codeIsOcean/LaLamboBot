from aiogram import Bot
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

admin_router = Router()


@admin_router.message(Command('start'))
async def msg_start(message: Message):
    admin_id = message.chat.id
    await message.answer(f'Hello, admin {admin_id}!')
