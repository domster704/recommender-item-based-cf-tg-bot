from dataclasses import asdict

import aiohttp

from src.domain.entities.raiting import Rating
from src.infrastructure.exceptions import InfrastructureError


class APIRatingRepository:
    def __init__(self, api_url: str):
        self.api_url = api_url.rstrip("/")

    async def add(self, rating: Rating):
        try:
            payload = {
                "tg_user_id": rating.user.tg_user_id,
                "movie_id": rating.movie.id,
                "rating": rating.rating,
            }

            async with aiohttp.ClientSession() as s:
                async with s.post(
                    f"{self.api_url}/v1/ratings/",
                    json=payload,
                ) as r:
                    if not r.ok:
                        raise InfrastructureError(
                            f"Ошибка при отправке рейтинга: {r.status}"
                        )
        except aiohttp.ClientError as e:
            raise InfrastructureError(f"Ошибка сети: {e}") from e
