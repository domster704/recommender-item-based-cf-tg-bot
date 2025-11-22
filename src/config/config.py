import platform

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from src.config.settings import settings

TOKEN = settings.bot_token
API_URL = settings.api_url
API_TOKEN = settings.api_key

if platform.system().lower().startswith("win"):
    # session = AiohttpSession(proxy="http://127.0.0.1:12334")
    session = AiohttpSession()
else:
    session = AiohttpSession()

bot = Bot(
    token=TOKEN,
    session=session,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()
