import aiohttp

from src.domain.entities.occupation import Occupation
from src.domain.entities.user import UserModel
from src.infrastructure.exceptions import InfrastructureError


class APIOccupationRepository:
    def __init__(self, api_url: str):
        self.api_url = api_url

    async def get_all(self) -> list[Occupation] | None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_url}/v1/occupations/") as response:
                    if not response.ok:
                        raise InfrastructureError(
                            f"Ошибка при получении списка профессий: {response.status}"
                        )
                    return await response.json()
        except aiohttp.ClientError as e:
            raise InfrastructureError(f"Ошибка сети: {e}") from e
