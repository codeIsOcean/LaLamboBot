import re  # импортируется чтобы искать строчку 12h
from aiogram import Bot, F, Dispatcher
from aiogram import Router
from aiogram.types import Message, ChatPermissions
from aiogram.filters import CommandStart, Command, CommandObject
from typing import Any
from aiogram.enums import ParseMode
from asyncpg.pgproto.pgproto import timedelta
from pydantic.v1.datetime_parse import parse_time
from contextlib import suppress  # импортируем чтобы забанить пользователя без ошибок
from aiogram.exceptions import TelegramBadRequest  # для игнорирования ошибок
from datetime import datetime, timedelta

from pyexpat.errors import messages
from pymorphy2 import MorphAnalyzer  # Устанавливается для анализа текста.

user_words_filter_router = Router()

morph = MorphAnalyzer()
ban_words = [
    r'клоун\w*', r'дура[кч]\w*', r'чмо\w*', r'ло[хш]\w*',
    r'пид[рa]\w*', r'\w+[е*.]*[eе]+[dд]+'
]


@user_words_filter_router.message(F.text)
async def filter_band_words(message: Message, bot: Bot) -> Any:
    # проверка является ли пользователь админом или простым юзером. Если админ то фильтр на него не действует
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status in ('administrator', 'creator'):
        return  # Пропускаем проверку для админов

    # проверка слов через морфологический анализатор
    for word in message.text.lower().strip().split():
        parsed_word = morph.parse(word)[0]
        normal_form = parsed_word.normal_form

        for pattern in ban_words:
            if re.search(pattern, normal_form, re.IGNORECASE):
                return await message.answer('🤬 не ругайся')

        for bad_word in ban_words:
            if bad_word in normal_form:
                return await message.answer('🤬 не ругайся')

    # дополнительная проверка всего текста
    for pattern in ban_words:
        if re.search(pattern, message.text, re.IGNORECASE):
            return await message.answer('Ну ну ну, не ругайся')
