from src.application.usecase.occupation.get_all import OccupationGetAllUseCase
from src.config.config import API_URL
from src.infrastructure.repositories.occupation_repository import (
    APIOccupationRepository,
)


def get_occupation_get_all_use_case():
    return OccupationGetAllUseCase(APIOccupationRepository(API_URL))
