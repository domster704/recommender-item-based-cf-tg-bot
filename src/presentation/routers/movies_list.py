import aiohttp
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from src.config.config import API_URL

movies_router = Router()

MOVIES_PER_PAGE = 5


async def load_movies():
    async with aiohttp.ClientSession() as s:
        async with s.get(f"{API_URL}/v1/movies/") as r:
            return await r.json()


@movies_router.message(F.text == "🎬 Список фильмов")
async def movies_start(message: Message, state: FSMContext):
    await state.update_data(page=0)
    await send_page(message, state)


async def send_page(message: Message, state: FSMContext):
    data = await state.get_data()
    page = data.get("page", 0)

    movies = await load_movies()
    total = len(movies)

    start = page * MOVIES_PER_PAGE
    end = start + MOVIES_PER_PAGE

    page_movies = movies[start:end]

    kb = InlineKeyboardBuilder()

    for m in page_movies:
        kb.button(text=m["title"], callback_data=f"movie_{m['id']}")

    nav_row = []
    if page > 0:
        kb.button(text="⬅ Назад", callback_data="page_prev")
    if end < total:
        kb.button(text="Далее ➡", callback_data="page_next")

    kb.adjust(1)

    await message.answer(
        f"Страница {page + 1}/{(total - 1) // MOVIES_PER_PAGE + 1}",
        reply_markup=kb.as_markup(),
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
