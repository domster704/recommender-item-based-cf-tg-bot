import aiohttp

from src.application.interfaces.user_repository import UserRepositoryABC
from src.domain.entities.user import UserModel
from src.domain.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
)
from src.infrastructure.exceptions import InfrastructureError


class APIUserRepository(UserRepositoryABC):
    def __init__(self, api_url: str):
        self.api_url = api_url

    async def add(
        self,
        tg_user_id: int,
        age: int | None = None,
        gender: str | None = None,
        occupation: dict | None = None,
    ) -> None:
        """
        Новый бэк требует:
        {
            "age": int | None,
            "gender": str | None,
            occupation: {
                id: int,
                name: str
            } | None,
            "tg_user_id": str
        }
        """

        payload = {
            "age": age,
            "gender": gender,
            "occupation": occupation,
            "tg_user_id": str(tg_user_id),
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/v1/users/",
                    json=payload,
                ) as response:
                    if response.status == 409:
                        raise UserAlreadyExistsError(
                            "Пользователь уже существует в базе"
                        )
                    if not response.ok:
                        raise InfrastructureError(
                            f"Ошибка при добавлении пользователя: {response.status}"
                        )
        except aiohttp.ClientError as e:
            raise InfrastructureError(f"Ошибка сети: {e}") from e

    async def get(self, tg_user_id: int) -> UserModel | None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/v1/users/{tg_user_id}",
                ) as response:
                    if response.status == 404:
                        raise UserNotFoundError(
                            f"Нет пользователя с user_id={tg_user_id}"
                        )
                    if not response.ok:
                        raise InfrastructureError(
                            f"Ошибка при получении пользователя: {response.status}"
                        )

                    data = await response.json()
                    print(data)
                    return UserModel(**data)
        except aiohttp.ClientError as e:
            raise InfrastructureError(f"Ошибка сети: {e}") from e

    async def update_user(self, data: dict) -> None:
        """
        {
            id: int | None,
            age: int | None,
            gender: str | None,
            occupation: {
                id: int,
                name: str
            } | None,
            tg_user_id: int
        }
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    f"{self.api_url}/v1/users/",
                    json=data,
                ) as response:
                    if not response.ok:
                        raise InfrastructureError("Ошибка обновления пользователя")
        except aiohttp.ClientError as e:
            raise InfrastructureError(f"Ошибка сети: {e}")
