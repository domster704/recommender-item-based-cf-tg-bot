from typing import Optional

from src.application.interfaces.user_repository import UserRepositoryABC
from src.domain.entities.user import UserModel
from src.domain.exceptions import UserAlreadyExistsError
from src.infrastructure.exceptions import InfrastructureError


class GrantTrialForUserUseCase:
    def __init__(self, repo: UserRepositoryABC):
        self.repo = repo

    async def grant_trial(self, tg_user_id: int) -> Optional[UserModel]:
        try:
            await self.repo.grant_trial(tg_user_id)
        except InfrastructureError as e_:
            raise
        except Exception as e__:
            raise InfrastructureError(str(e__))
