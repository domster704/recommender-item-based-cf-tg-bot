import aiohttp

from src.application.interfaces.user_repository import UserRepositoryABC
from src.domain.entities.user import UserModel
from src.domain.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
)
from src.infrastructure.exceptions import InfrastructureError


class ApiUserRepository(UserRepositoryABC):
    def __init__(self, api_url: str, api_token: str):
        self.api_url = api_url
        self.api_token = api_token

    async def add(self, tg_user_id: int) -> None:
        """

        Args:
            tg_user_id:

        Returns:

        Raises:
            InfrastructureError: Ошибка сети
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        f"{self.api_url}/v1/user/",
                        json={"tg_user_id": str(tg_user_id)},
                        headers={
                            "Authorization": f"Bearer {self.api_token}",
                        },
                ) as response:
                    if response.status == 409:
                        raise UserAlreadyExistsError(
                            "Пользователь уже существует в базе"
                        )
        except aiohttp.ClientError as e:
            raise InfrastructureError(f"Ошибка сети: {e}") from e

    async def grant_trial(self, tg_user_id: int) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        f"{self.api_url}/v1/subscription/trial",
                        json={"user_id": str(tg_user_id)},
                        headers={
                            "Authorization": f"Bearer {self.api_token}",
                        },
                ) as response:
                    if not response.ok:
                        raise InfrastructureError(
                            "Ошибка при активации пробного периода"
                        )
                    if response.status == 208:
                        raise UserAlreadyExistsError(
                            "Пользователь уже активирован пробный период"
                        )
                    return None
        except aiohttp.ClientError as e:
            raise InfrastructureError(f"Ошибка сети: {e}") from e

    async def register(self, user: UserModel) -> None:
        """

        Args:
            user:
        Returns:

        Raises:
            UserAlreadyExistsError: Пользователь уже зарегистрирован
            InfrastructureError: Ошибка сети

        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        f"{self.api_url}/v1/user/register",
                        json={
                            "phone": user.phone,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "user_id": str(user.tg_user_id),
                        },
                        headers={
                            "Authorization": f"Bearer {self.api_token}",
                        },
                ) as response:
                    if response.status == 409:
                        raise UserAlreadyExistsError("Пользователь уже зарегистрирован")
        except aiohttp.ClientError as e:
            raise InfrastructureError(f"Ошибка сети: {e}") from e

    async def get(self, tg_user_id: int) -> UserModel | None:
        """

        Args:
            tg_user_id:

        Returns:

        Raises:
            UserNotFoundError: Пользователь не найден
            InfrastructureError: Ошибка сети
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"{self.api_url}/v1/user/{tg_user_id}",
                        headers={
                            "Authorization": f"Bearer {self.api_token}",
                        },
                ) as response:
                    if response.status == 404:
                        raise UserNotFoundError(
                            f"Нет пользователя с user_id={tg_user_id}"
                        )
                    if not response.ok:
                        print(await response.text())
                        raise InfrastructureError(
                            f"Ошибка при получении пользователя: {response.status}"
                        )

                    data = await response.json()
                    return UserModel(**data)
        except aiohttp.ClientError as e:
            raise InfrastructureError(f"Ошибка сети: {e}") from e

    async def update_user(self, tg_user_id: int, data: dict) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(
                        f"{self.api_url}/v1/user/{tg_user_id}",
                        json=data,
                        headers={"Authorization": f"Bearer {self.api_token}"}
                ) as response:
                    if not response.ok:
                        raise InfrastructureError("Ошибка обновления пользователя")
        except aiohttp.ClientError as e:
            raise InfrastructureError(f"Ошибка сети: {e}")
