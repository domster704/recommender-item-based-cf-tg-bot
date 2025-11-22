import aiohttp
from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config.config import API_URL, API_TOKEN

recommend_router = Router()


@recommend_router.message(F.text == "🎬 Получить рекомендации")
async def get_recommendations(message: Message):
    tg_id = message.from_user.id

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{API_URL}/v1/recommendations/{tg_id}",
                headers={"Authorization": f"Bearer {API_TOKEN}"}
        ) as r:
            if not r.ok:
                await message.answer("Не удалось получить рекомендации")
                return

            movie_ids = await r.json()

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/v1/movies/") as r:
            movies = await r.json()

    movie_map = {m["id"]: m for m in movies}
    text = "🎬 Вот фильмы, которые подходят тебе:\n\n"

    for mid in movie_ids:
        m = movie_map.get(mid)
        if not m:
            continue
        text += f"• <b>{m['title']}</b> ({m['release_date']})\n"

    kb = InlineKeyboardBuilder()
    # TODO: add rate buttons
    kb.button(text="(+) Нравится", callback_data="rate_5")
    kb.button(text="(~) Нормально", callback_data="rate_3")
    kb.button(text="(-) Не понравилось", callback_data="rate_1")
    kb.adjust(3)

    await message.answer(text, reply_markup=kb.as_markup())
