class UserGetUseCase:
    def __init__(self, repo):
        self.repo = repo

    async def execute(self, tg_user_id: int):
        return await self.repo.get(tg_user_id)
