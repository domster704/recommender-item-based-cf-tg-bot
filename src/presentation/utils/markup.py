from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config.settings import settings


async def generateMarkupWithWebApp(
    state_data: dict, state: FSMContext
) -> InlineKeyboardBuilder:
    url = settings.front_url

    markup = InlineKeyboardBuilder()
    markup.row(
        InlineKeyboardButton(text="Novikov TV Club", web_app=WebAppInfo(url=url))
    )
    return markup
