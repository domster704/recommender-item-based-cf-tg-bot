from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.config.config import API_URL, API_TOKEN
from src.infrastructure.repositories.user_repository import APIUserRepository
from src.presentation.dependencies.occupation import get_occupation_get_all_use_case
from src.presentation.dependencies.user import (
    get_user_get_use_case,
    get_user_update_occupation_use_case,
)
from src.presentation.keyboards.menu import main_menu_keyboard
from src.presentation.keyboards.occupations import occupations_keyboard

menu_router = Router()


class EditOccupation(StatesGroup):
    waiting = State()


@menu_router.message(F.text == "Профиль")
async def profile(message: Message):
    user = await get_user_get_use_case().execute(message.from_user.id)

    kb = ReplyKeyboardBuilder()
    kb.button(text="Изменить occupation")
    kb.button(text="Назад")

    text = f"""
<b>Ваш профиль</b>
Occupation: {user.occupation}
Age: {user.age}
Gender: {user.gender}
"""

    await message.answer(text, reply_markup=kb.as_markup(resize_keyboard=True))


@menu_router.message(F.text == "Назад")
async def back(message: Message):
    await message.answer("Главное меню:", reply_markup=main_menu_keyboard())


@menu_router.message(F.text == "Изменить occupation")
async def ask_occupation(message: Message, state: FSMContext):
    occupations = await get_occupation_get_all_use_case().execute()
    await state.update_data(occupations=occupations)
    await state.set_state(EditOccupation.waiting)

    await message.answer(
        "Выберите новую профессию:", reply_markup=occupations_keyboard(occupations)
    )


@menu_router.message(EditOccupation.waiting)
async def update_occupation(message: Message, state: FSMContext):
    occupations = (await state.get_data())["occupations"]
    selected = next((o for o in occupations if o["name"] == message.text), None)

    if not selected:
        await message.answer("Выберите профессию из предложенных.")
        return

    uc = get_user_update_occupation_use_case()
    await uc.execute(message.from_user.id, selected)

    await state.clear()
    await message.answer(
        f"Профессия обновлена на {selected['name']}",
        reply_markup=main_menu_keyboard(),
    )
