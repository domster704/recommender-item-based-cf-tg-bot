from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.config.config import API_URL, API_TOKEN
from src.infrastructure.repositories.user_repository import ApiUserRepository
from src.presentation.keyboards.menu import main_menu_keyboard

menu_router = Router()
repo = ApiUserRepository(API_URL, API_TOKEN)


class EditOccupation(StatesGroup):
    waiting = State()


@menu_router.message(F.text == "🧾 Профиль")
async def profile(message: Message):
    tg_id = message.from_user.id
    user = await repo.get(tg_id)

    text = f"""
<b>Ваш профиль</b>

Occupation: {user.__dict__.get("occupation")}
Age: {user.__dict__.get("age")}
Gender: {user.__dict__.get("gender")}

Что хотите изменить?
"""

    kb = ReplyKeyboardBuilder()
    kb.button(text="🔧 Изменить occupation")
    kb.button(text="🔙 Назад")
    await message.answer(text, reply_markup=kb.as_markup(resize_keyboard=True))


@menu_router.message(F.text == "🔙 Назад")
async def back(message: Message):
    await message.answer("Главное меню:", reply_markup=main_menu_keyboard())


@menu_router.message(F.text == "🔧 Изменить occupation")
async def ask_occ(message: Message, state: FSMContext):
    await state.set_state(EditOccupation.waiting)
    await message.answer("Введите новую occupation:")


@menu_router.message(EditOccupation.waiting)
async def update_occ(message: Message, state: FSMContext):
    new_occ = message.text
    tg_id = message.from_user.id

    await repo.update_user(tg_id, {"occupation": new_occ})

    await message.answer(
        "Occupation обновлена!",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()
