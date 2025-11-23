from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from src.config.config import API_URL
from src.domain.entities.occupation import Occupation
from src.domain.entities.user import UserGender
from src.domain.exceptions import UserNotFoundError
from src.infrastructure.exceptions import InfrastructureError
from src.infrastructure.repositories.occupation_repository import (
    APIOccupationRepository,
)
from src.presentation.dependencies.occupation import get_occupation_get_all_use_case
from src.presentation.dependencies.user import (
    get_user_get_use_case,
    get_user_register_use_case,
)
from src.presentation.keyboards.gender import gender_keyboard
from src.presentation.keyboards.menu import main_menu_keyboard
from src.presentation.keyboards.occupations import occupations_keyboard

start_router = Router()


class UserRegistrationState(StatesGroup):
    gender = State()
    age = State()
    occupation = State()


@start_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    user_get = get_user_get_use_case()

    try:
        await user_get.execute(message.from_user.id)
        await message.answer("Добро пожаловать!", reply_markup=main_menu_keyboard())
        return

    except UserNotFoundError:
        await message.answer(
            "Для начала создадим профиль. Выберите пол:",
            reply_markup=gender_keyboard(),
        )
        await state.set_state(UserRegistrationState.gender)


@start_router.message(UserRegistrationState.gender)
async def process_gender(message: Message, state: FSMContext):
    txt = message.text.lower()

    if txt == "мужской":
        gender = UserGender.M
    elif txt == "женский":
        gender = UserGender.F
    else:
        await message.answer("Пожалуйста, выберите пол с клавиатуры.")
        return

    await state.update_data(gender=gender)

    await message.answer("Введите ваш возраст (число):", reply_markup=None)
    await state.set_state(UserRegistrationState.age)


@start_router.message(UserRegistrationState.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите возраст числом:")
        return

    age = int(message.text)

    await state.update_data(age=age)

    occupation_uc = get_occupation_get_all_use_case()

    try:
        occupations = await occupation_uc.execute()
    except InfrastructureError:
        await message.answer("Не удалось загрузить список профессий.")
        return

    await state.update_data(occupations=occupations)

    await message.answer(
        "Выберите вашу профессию:", reply_markup=occupations_keyboard(occupations)
    )

    await state.set_state(UserRegistrationState.occupation)


@start_router.message(UserRegistrationState.occupation)
async def process_occupation(message: Message, state: FSMContext):
    data = await state.get_data()
    occupations = data["occupations"]

    selected = next((o for o in occupations if o["name"] == message.text), None)
    if not selected:
        await message.answer("Выберите профессию из списка.")
        return

    uc = get_user_register_use_case()

    await uc.execute(
        tg_user_id=message.from_user.id,
        age=data["age"],
        gender=data["gender"].value,
        occupation=selected,
    )

    await state.clear()
    await message.answer("Профиль создан!", reply_markup=main_menu_keyboard())
