import aiohttp
from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.config.config import API_URL, API_TOKEN

ratings_router = Router()


async def send_rating(user_id: int, movie_id: int, rating: int):
    async with aiohttp.ClientSession() as s:
        await s.post(
            f"{API_URL}/v1/ratings/",
            json={"user_id": str(user_id), "movie_id": str(movie_id), "rating": rating},
            headers={"Authorization": f"Bearer {API_TOKEN}"},
        )


@ratings_router.callback_query(F.data.startswith("rate_"))
async def rate(callback: CallbackQuery):
    _, movie_id, rating = callback.data.split("_")
    movie_id = int(movie_id)
    rating = int(rating)

    user_id = callback.from_user.id
    await send_rating(user_id, movie_id, rating)

    await callback.answer("Спасибо, оценка сохранена!")
    await callback.message.answer("⭐ Оценка сохранена!")
