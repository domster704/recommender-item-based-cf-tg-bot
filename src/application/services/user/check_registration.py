from typing import Optional

from src.application.interfaces.user_repository import UserRepositoryABC
from src.domain.entities.user import UserModel
from src.domain.exceptions import UserNotFoundError
from src.infrastructure.exceptions import InfrastructureError


class CheckRegistrationUseCase:
    def __init__(self, user_repository: UserRepositoryABC):
        self.repo = user_repository

    async def execute(self, tg_user_id: int) -> Optional[UserModel]:
        try:
            user = await self.repo.get(tg_user_id)
            if not user.is_registered():
                return None

            return user
        except UserNotFoundError as e:
            await self.repo.add(tg_user_id)
            return None
        except InfrastructureError as e_:
            raise
