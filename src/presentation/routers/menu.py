from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.config.config import API_URL, API_TOKEN
from src.infrastructure.exceptions import InfrastructureError
from src.infrastructure.repositories.occupation_repository import (
    APIOccupationRepository,
)
from src.infrastructure.repositories.user_repository import APIUserRepository
from src.presentation.keyboards.menu import main_menu_keyboard
from src.presentation.keyboards.occupations import occupations_keyboard

menu_router = Router()
repo = APIUserRepository(API_URL, API_TOKEN)


class EditOccupation(StatesGroup):
    waiting = State()


@menu_router.message(F.text == "Профиль")
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
    kb.button(text="Изменить occupation")
    kb.button(text="Назад")
    await message.answer(text, reply_markup=kb.as_markup(resize_keyboard=True))


@menu_router.message(F.text == "Назад")
async def back(message: Message):
    await message.answer("Главное меню:", reply_markup=main_menu_keyboard())


@menu_router.message(F.text == "Изменить occupation")
async def ask_occ(message: Message, state: FSMContext):
    repo = APIOccupationRepository(API_URL)

    try:
        occupations = await repo.get_all()
    except InfrastructureError as e:
        await message.answer("Не удалось загрузить список профессий. Попробуйте позже.")
        return

    await state.update_data(occupations=occupations)

    await state.set_state(EditOccupation.waiting)
    await message.answer(
        "Выберите новую профессию:", reply_markup=occupations_keyboard(occupations)
    )


@menu_router.message(EditOccupation.waiting)
async def update_occ(message: Message, state: FSMContext):
    data = await state.get_data()
    occupations = data["occupations"]

    selected = next((o for o in occupations if o["name"] == message.text), None)

    if selected is None:
        await message.answer("Пожалуйста, выберите профессию с клавиатуры.")
        return

    tg_id = message.from_user.id

    user = await repo.get(tg_id)

    payload = {
        "id": user.id,
        "age": user.age,
        "gender": user.gender,
        "occupation": {"id": selected["id"], "name": selected["name"]},
        "tg_user_id": tg_id,
    }

    try:
        await repo.update_user(payload)
    except InfrastructureError as e:
        await message.answer("Ошибка при обновлении профессии.")
        return

    await message.answer(
        f"Профессия обновлена на: <b>{selected['name']}</b>",
        reply_markup=main_menu_keyboard(),
    )

    await state.clear()
