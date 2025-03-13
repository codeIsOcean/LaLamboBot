import os

from aiohttp.helpers import TOKEN
from dotenv import load_dotenv

load_dotenv()  # загружаем env в невидимом виде

TOKEN = os.getenv('TOKEN')
