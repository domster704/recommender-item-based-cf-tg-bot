from src.domain.entities.movie import Movie
from src.infrastructure.repositories.movie_repository import APIMovieRepository


class MovieGetByIdUseCase:
    def __init__(self, repo: APIMovieRepository):
        self.repo = repo

    async def execute(self, movie_id: int) -> Movie:
        return await self.repo.get_by_id(movie_id)
