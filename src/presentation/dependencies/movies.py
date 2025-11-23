from src.application.services.movies.get_all import MoviesGetAllUseCase
from src.application.services.movies.get_by_id import MovieGetByIdUseCase

from src.config.config import API_URL
from src.infrastructure.repositories.movie_repository import APIMovieRepository


def get_movies_use_case():
    return MoviesGetAllUseCase(APIMovieRepository(API_URL))


def get_movie_by_id_use_case():
    return MovieGetByIdUseCase(APIMovieRepository(API_URL))
