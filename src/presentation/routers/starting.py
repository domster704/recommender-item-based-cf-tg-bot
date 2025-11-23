from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from src.config.config import API_URL, API_TOKEN
from src.domain.entities.occupation import Occupation
from src.domain.entities.user import UserGender
from src.domain.exceptions import UserNotFoundError
from src.infrastructure.exceptions import InfrastructureError
from src.infrastructure.repositories.occupation_repository import (
    APIOccupationRepository,
)
from src.infrastructure.repositories.user_repository import APIUserRepository
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
    repo = APIUserRepository(API_URL, API_TOKEN)

    try:
        await repo.get(message.from_user.id)

        await message.answer(
            "Добро пожаловать! Я помогу подобрать фильмы.\nВыберите действие:",
            reply_markup=main_menu_keyboard(),
        )
        return

    except UserNotFoundError:
        await message.answer(
            "Для начала подберите профиль.\nВыберите ваш пол:",
            reply_markup=gender_keyboard(),
        )
        await state.set_state(UserRegistrationState.gender)

    except InfrastructureError:
        await message.answer("Ошибка подключения к серверу. Попробуйте позже.")


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
    if not (1 <= age <= 120):
        await message.answer("Возраст должен быть от 1 до 120.")
        return

    await state.update_data(age=age)

    repo = APIOccupationRepository(API_URL)

    try:
        occupations: list[Occupation] = await repo.get_all()
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

    selected: Occupation | None = next(
        (o for o in occupations if o["name"] == message.text), None
    )

    if selected is None:
        await message.answer("Пожалуйста, выберите профессию из списка.")
        return

    await state.update_data(occupation=selected)

    gender = data["gender"]
    age = data["age"]
    occupation = selected

    repo = APIUserRepository(API_URL, API_TOKEN)

    try:
        await repo.add(
            tg_user_id=message.from_user.id,
            age=age,
            gender=gender.value,
            occupation=occupation,
        )
    except InfrastructureError:
        await message.answer("Ошибка при сохранении профиля. Попробуйте позже.")
        return

    await state.clear()

    await message.answer(
        "Профиль создан! Теперь я могу подбирать вам фильмы.",
        reply_markup=main_menu_keyboard(),
    )
