from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.config.config import API_URL, API_TOKEN
from src.infrastructure.exceptions import InfrastructureError
from src.infrastructure.repositories.user_repository import ApiUserRepository
from src.presentation.keyboards.menu import main_menu_keyboard

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    repo = ApiUserRepository(API_URL, API_TOKEN)

    try:
        await repo.add(message.from_user.id)
    except InfrastructureError as e:
        pass

    await state.update_data(page=0)

    await message.answer(
        "Добро пожаловать! Я помогу подобрать фильмы.\nВыберите действие:",
        reply_markup=main_menu_keyboard()
    )
