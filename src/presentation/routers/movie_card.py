from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.domain.entities.movie import Movie
from src.presentation.dependencies.movies import get_movie_by_id_use_case
from src.presentation.routers.movies_list import MovieCallbackData

movie_card_router = Router()


@movie_card_router.callback_query(MovieCallbackData.filter())
async def movie_selected(callback: CallbackQuery, callback_data: MovieCallbackData):
    movie_id: int = callback_data.id

    use_case = get_movie_by_id_use_case()
    movie: Movie = await use_case.execute(movie_id)

    genres = ", ".join(g.name for g in movie.genres)

    text = f"""
<b>{movie.title}</b>
Дата выхода: {movie.release_date}

Жанры: {genres}

Ссылка IMDb: {movie.imdb_url}
"""

    kb = InlineKeyboardBuilder()
    for i in range(1, 6):
        kb.button(text=str(i), callback_data=f"rate_{movie_id}_{i}")
    kb.adjust(5)

    await callback.message.answer(text, reply_markup=kb.as_markup())
