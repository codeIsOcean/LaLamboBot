import re  # импортируется чтобы искать строчку 12h
from aiogram import Bot, F, Dispatcher
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CommandObject
from typing import Any
from aiogram.enums import ParseMode
from asyncpg.pgproto.pgproto import timedelta
from pydantic.v1.datetime_parse import parse_time
from contextlib import suppress  # импортируем чтобы забанить пользователя без ошибок
from aiogram.exceptions import TelegramBadRequest  # для игнорирования ошибок
from datetime import datetime, timedelta

from configs import ADMIN_IDS

admin_router = Router()
# проверяем что это группа и то что в группе пишет админ, только в этом случае команда /ban работает
admin_router.message.filter(F.chat.type.in_({'supergroup', 'group'}), F.from_user.id.in_(ADMIN_IDS))


# функция для генераций datetime обьекта
def parse_time(time_string: str | None) -> datetime | None:
    if not time_string:
        return None

    match_ = re.match(r'(\d+)([a-z])',
                      time_string.lower().strip())  # \d+ , d тут значит цифры а d+ значит несколько цифр,
    current_datetime = datetime.utcnow()
    # [a-z] будем искать все буквы от а до z
    if match_:
        # group(1) => 12, group(2) => h
        value, unit = int(match_.group(1)), match_.group(2)

        match unit:
            # timedelta можем прибавить к нашей текущей дате, другую дату
            case 'h':
                time_delta = timedelta(hours=value)
            case 'd':
                time_delta = timedelta(days=value)
            case 'w':
                time_delta = timedelta(weeks=value)
            case _:
                return None
    else:
        return None

    new_datetime = current_datetime + time_delta
    return new_datetime  # если указали 4w, если сегодня 17 марта + 4 недели будет 17 апреля


# Реакция бота на команду /start
@admin_router.message(Command('start'))
async def msg_start(message: Message):
    admin_id = message.chat.id
    await message.answer(f'Hello, admin {admin_id}!')


# Ручная команда /ban
@admin_router.message(Command('ban'))
async def ban_cmd(message: Message, bot: Bot, command: CommandObject | None) -> Any:
    # в переменной reply сохраниться информация про пользователя которого мы процетировали
    reply = message.reply_to_message
    # Если ответ пустой то возращяем None
    if not reply:
        return None
    until_date = parse_time(command.args)  # parse_time парсит время бана, (command.args) 12 h распознает время бана
    mention = reply.from_user.mention_html(reply.from_user.first_name)

    # игнорируем ошибку при команде /ban возникает когда пытаемся забанить пользователя с правами админа
    with suppress(TelegramBadRequest):
        await bot.ban_chat_member(
            chat_id=message.chat.id, user_id=reply.from_user.id, until_date=until_date
        )
        await message.answer(f'😱 Пользователь <b>{mention}</b> забанили')
