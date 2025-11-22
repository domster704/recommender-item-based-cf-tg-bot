import aiohttp
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config.config import API_URL

movie_card_router = Router()


async def load_movie(movie_id: int):
    async with aiohttp.ClientSession() as s:
        async with s.get(f"{API_URL}/v1/movies/{movie_id}") as r:
            return await r.json()


@movie_card_router.callback_query(F.data.startswith("movie_"))
async def open_movie(callback: CallbackQuery):
    movie_id = int(callback.data.split("_")[1])

    movie = await load_movie(movie_id)

    text = f"""
<b>{movie['title']}</b> ({movie['release_date']})

Жанры: {", ".join(movie['genres'])}
Описание: {movie['overview']}
"""

    kb = InlineKeyboardBuilder()
    for i in range(1, 6):
        kb.button(text=str(i), callback_data=f"rate_{movie_id}_{i}")
    kb.adjust(5)

    await callback.message.answer(text, reply_markup=kb.as_markup())
