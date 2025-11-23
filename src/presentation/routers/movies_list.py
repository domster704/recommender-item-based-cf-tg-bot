from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.dependencies.movies import get_movies_use_case

movies_router = Router()

MOVIES_PER_PAGE = 5


@movies_router.message(F.text == "Список фильмов")
async def movies_start(message: Message, state: FSMContext):
    await state.update_data(page=0)
    await send_page(message, state)


async def send_page(message: Message, state: FSMContext):
    data = await state.get_data()
    page = data.get("page", 0)

    movies_uc = get_movies_use_case()
    movies = await movies_uc.execute()

    total = len(movies)
    start = page * MOVIES_PER_PAGE
    end = start + MOVIES_PER_PAGE
    page_movies = movies[start:end]

    keyboard = InlineKeyboardBuilder()

    for movie in page_movies:
        keyboard.button(text=movie.title, callback_data=f"movie_{movie.id}")

    keyboard.adjust(1)

    nav_row = []

    if page > 0:
        nav_row.append(
            InlineKeyboardBuilder()
            .button(text="⬅ Назад", callback_data="page_prev")
            .as_markup().inline_keyboard[0][0]
        )

    if end < total:
        nav_row.append(
            InlineKeyboardBuilder()
            .button(text="Вперёд ➡", callback_data="page_next")
            .as_markup().inline_keyboard[0][0]
        )

    if nav_row:
        keyboard.row(*nav_row)

    await message.answer(
        f"Страница {page + 1}/{(total - 1) // MOVIES_PER_PAGE + 1}",
        reply_markup=keyboard.as_markup(),
    )


@movies_router.callback_query(F.data == "page_prev")
async def prev(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = max(0, data.get("page", 0) - 1)
    await state.update_data(page=page)

    await callback.message.delete()
    await send_page(callback.message, state)


@movies_router.callback_query(F.data == "page_next")
async def next_(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data.get("page", 0) + 1
    await state.update_data(page=page)

    await callback.message.delete()
    await send_page(callback.message, state)
