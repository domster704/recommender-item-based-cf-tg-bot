from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.domain.entities.movie import Movie
from src.presentation.dependencies.movies import get_movies_use_case
from src.presentation.keyboards.pagination import PaginationItems, Pagination

movies_router = Router()

MOVIES_PER_PAGE = 5


class MovieCallbackData(CallbackData, prefix="movie"):
    id: int


@movies_router.message(F.text == "Список фильмов")
async def movies_start(message: Message, state: FSMContext):
    movies_uc = get_movies_use_case()
    movies: list[Movie] = await movies_uc.execute()

    items: list[PaginationItems] = []
    for m in movies:
        items.append(
            PaginationItems(text=m.title, callback_data=MovieCallbackData(id=m.id))
        )

    pagination = Pagination(
        items=items,
        max_items_per_page=MOVIES_PER_PAGE,
        callback_data_navigation_ending="movies",
    )

    await state.update_data(pagination=pagination)

    await message.answer(text="Список фильмов:", reply_markup=pagination.get_markup())
