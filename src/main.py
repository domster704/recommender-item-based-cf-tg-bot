import asyncio

from src.config.config import bot, dp
from src.presentation.keyboards.pagination import pagination_router
from src.presentation.routers.menu import menu_router
from src.presentation.routers.movie_card import movie_card_router
from src.presentation.routers.movies_list import movies_router
from src.presentation.routers.ratings import ratings_router
from src.presentation.routers.starting import start_router


async def main() -> None:
    dp.include_routers(
        pagination_router,
        start_router,
        menu_router,
        movies_router,
        movie_card_router,
        ratings_router,
    )
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
