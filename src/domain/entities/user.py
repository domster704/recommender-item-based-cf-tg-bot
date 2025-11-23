from enum import StrEnum

from pydantic import BaseModel

from src.domain.entities.occupation import Occupation


class UserGender(StrEnum):
    M = "male"
    F = "female"


class UserModel(BaseModel):
    id: int | None
    age: int
    gender: UserGender
    occupation: Occupation | None
    tg_user_id: int | None = None
