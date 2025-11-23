class MoviesGetAllUseCase:
    def __init__(self, repo):
        self.repo = repo

    async def execute(self):
        return await self.repo.get_all()
