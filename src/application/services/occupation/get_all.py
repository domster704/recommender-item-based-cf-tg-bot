class OccupationGetAllUseCase:
    def __init__(self, occ_repo):
        self.occ_repo = occ_repo

    async def execute(self):
        return await self.occ_repo.get_all()
