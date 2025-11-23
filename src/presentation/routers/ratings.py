from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.domain.entities.movie import Movie
from src.domain.entities.raiting import Rating
from src.domain.entities.user import UserModel
from src.presentation.dependencies.movies import get_movie_by_id_use_case
from src.presentation.dependencies.ratings import get_rating_create_use_case
from src.presentation.dependencies.user import get_user_get_use_case

ratings_router = Router()


@ratings_router.callback_query(F.data.startswith("rate_"))
async def rate(callback: CallbackQuery):
    _, movie_id, rating_value = callback.data.split("_")
    movie_id = int(movie_id)
    rating_value = int(rating_value)

    tg_user_id = callback.from_user.id

    user_uc = get_user_get_use_case()
    movie_uc = get_movie_by_id_use_case()
    rating_uc = get_rating_create_use_case()

    user: UserModel = await user_uc.execute(tg_user_id)
    movie: Movie = await movie_uc.execute(movie_id)

    rating = Rating(user=user, movie=movie, rating=rating_value, timestamp=None)

    await rating_uc.execute(rating)

    await callback.message.answer("Оценка сохранена!")
