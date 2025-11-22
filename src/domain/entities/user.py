from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    tg_user_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]

    def is_registered(self) -> bool:
        return self.phone is not None
