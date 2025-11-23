import aiohttp

from src.domain.entities.movie import Movie, Genre
from src.infrastructure.exceptions import InfrastructureError


class APIMovieRepository:
    def __init__(self, api_url: str):
        self.api_url = api_url.rstrip("/")

    async def get_all(self) -> list[Movie]:
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(f"{self.api_url}/v1/movies/") as r:
                    if not r.ok:
                        raise InfrastructureError(f"Ошибка загрузки фильмов: {r.status}")

                    data = await r.json()

            movies = [
                Movie(
                    id=m["id"],
                    title=m["title"],
                    release_date=m["release_date"],
                    video_release_date=m["video_release_date"],
                    imdb_url=m["imdb_url"],
                    genres=[
                        Genre(id=g["id"], name=g["name"])
                        for g in m["genres"]
                    ]
                ) for m in data
            ]

            return movies

        except Exception as e:
            raise InfrastructureError(f"Ошибка при загрузке фильмов: {e}")

    async def get_by_id(self, movie_id: int) -> Movie:
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(f"{self.api_url}/v1/movies/{movie_id}") as r:
                    if not r.ok:
                        raise InfrastructureError(f"Ошибка загрузки фильма: {r.status}")

                    data = await r.json()

            movie = Movie(
                id=data["id"],
                title=data["title"],
                release_date=data["release_date"],
                video_release_date=data["video_release_date"],
                imdb_url=data["imdb_url"],
                genres=[
                    Genre(id=g["id"], name=g["name"])
                    for g in data["genres"]
                ]
            )

            return movie

        except Exception as e:
            raise InfrastructureError(f"Ошибка при загрузке фильма: {e}")
