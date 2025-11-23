class UserUpdateOccupationUseCase:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    async def execute(self, tg_user_id: int, occupation):
        user = await self.user_repo.get(tg_user_id)

        payload = {
            "id": user.id,
            "age": user.age,
            "gender": user.gender,
            "occupation": {"id": occupation["id"], "name": occupation["name"]},
            "tg_user_id": tg_user_id,
        }

        await self.user_repo.update_user(payload)
