import re
from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.enums.chat_member_status import ChatMemberStatus
from pymorphy2 import MorphAnalyzer

user_words_filter_router = Router()
morph = MorphAnalyzer()

ban_words = {
    'клоун', 'дурак', 'чмо', 'лох', 'лош', 'пидр', 'weed', 'сука', 'лошара', 'ешак'
}

# Символы, которые могут использоваться для обхода фильтра
replacements = {
    'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x',
    '0': 'o', '1': 'l', '3': 'e', '.': '', '*': '', ' ': '', '-': '', '_': '',
    '!': '', '@': '', '#': '', '$': '', '%': '', '^': '', '&': '', '=': '', '+': ''
}

# Регулярные выражения для поиска ссылок
telegram_link_pattern = r"(?:https?://)?(?:t\.me|telegram\.me)/[\w+]+|@\w+"
url_pattern = r"(?:https?://|www\.)\S+"


@user_words_filter_router.message()
async def filter_bad_words(message: Message, bot: Bot):
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
        return  # Пропускаем админом

    text = message.text.lower().strip()  # получаемое смс приводим в нижний регистр и чищем

    # Удаляем пробелы, символы и заменяем буквы
    normolized_text = text
    for rus, eng in replacements.items():
        normolized_text = normolized_text.replace(rus, eng)

    # Проверяем каждое слово, приведенное к нормальной форме
    words = text.split()
    normolized_words = {morph.parse(word)[0].normal_form for word in words}

    # Фильтр запрешенных слов
    if any(bad_word in normolized_text for bad_word in ban_words) or \
            any(bad_word in normolized_words for bad_word in ban_words):
        await message.delete()  # удаляем запрешенно сообшение
        await message.answer(f'🛑 {message.from_user.first_name}, не ругайся!')

    # Фильтр телеграм-ссылок и любых других ссылок
    elif re.search(telegram_link_pattern, text) or re.search(url_pattern, text):
        await message.delete()
        await message.answer(f'⛔ {message.from_user.first_name}, ссылки запрешенны')


# Прежний код
# @user_words_filter_router.message(F.text)
# async def filter_band_words(message: Message, bot: Bot) -> Any:
#     # проверка является ли пользователь админом или простым юзером. Если админ то фильтр на него не действует
#     chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
#     if chat_member.status in ('administrator', 'creator'):
#         return  # Пропускаем проверку для админов
#
#     # проверка слов через морфологический анализатор
#     for word in message.text.lower().strip().split():
#         parsed_word = morph.parse(word)[0]
#         normal_form = parsed_word.normal_form
#
#         for pattern in ban_words:
#             if re.search(pattern, normal_form, re.IGNORECASE):
#                 return await message.answer('🤬 не ругайся')
#
#         for bad_word in ban_words:
#             if bad_word in normal_form:
#                 return await message.answer('🤬 не ругайся')
#
#     # дополнительная проверка всего текста
#     for pattern in ban_words:
#         if re.search(pattern, message.text, re.IGNORECASE):
#             return await message.answer('Ну ну ну, не ругайся')
