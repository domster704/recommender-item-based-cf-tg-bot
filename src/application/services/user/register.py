from typing import Optional

from src.application.interfaces.user_repository import UserRepositoryABC
from src.domain.entities.user import UserModel
from src.domain.exceptions import UserAlreadyExistsError
from src.infrastructure.exceptions import InfrastructureError


class RegisterUserUseCase:
    def __init__(self, repo: UserRepositoryABC):
        self.repo = repo

    async def register(
        self, tg_user_id: int, phone: str, first_name: str, last_name: str
    ) -> Optional[UserModel]:
        user = UserModel(
            tg_user_id=tg_user_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=None,
        )

        try:
            await self.repo.register(user)
            return user
        except UserAlreadyExistsError as e:
            raise
        except InfrastructureError as e_:
            raise
        except Exception as e__:
            raise InfrastructureError(str(e__))
