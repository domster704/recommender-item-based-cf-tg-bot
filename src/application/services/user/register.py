class UserRegisterUseCase:
    def __init__(self, repo):
        self.repo = repo

    async def execute(self, tg_user_id: int, age: int, gender: str, occupation):
        await self.repo.add(
            tg_user_id=tg_user_id, age=age, gender=gender, occupation=occupation
        )
