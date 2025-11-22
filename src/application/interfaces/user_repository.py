from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.user import UserModel


class UserRepositoryABC(ABC):
    """Абстракция репозитория пользователя"""

    @abstractmethod
    async def add(self, tg_user_id: int) -> None:
        """Создать пустого пользователя до регистрации"""
        pass

    @abstractmethod
    async def register(self, user: UserModel) -> None:
        """Зарегистрировать пользователя с полными данными"""
        pass

    @abstractmethod
    async def get(self, tg_user_id: int) -> Optional[UserModel]:
        """Получить пользователя по Telegram ID"""
        pass

    @abstractmethod
    async def grant_trial(self, tg_user_id: int) -> None:
        """Выдать пробный доступ пользователю"""
        pass
