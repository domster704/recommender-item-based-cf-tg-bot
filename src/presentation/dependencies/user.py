from src.application.services.user.get import UserGetUseCase
from src.application.services.user.register import UserRegisterUseCase
from src.application.services.user.update import UserUpdateOccupationUseCase
from src.config.config import API_URL
from src.infrastructure.repositories.user_repository import APIUserRepository


def get_user_get_use_case():
    return UserGetUseCase(APIUserRepository(API_URL))


def get_user_register_use_case():
    return UserRegisterUseCase(APIUserRepository(API_URL))


def get_user_update_occupation_use_case():
    return UserUpdateOccupationUseCase(APIUserRepository(API_URL))
