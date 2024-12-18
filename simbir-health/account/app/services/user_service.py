from app.repositories.user_repository import IUserRepository


class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def get_user(self, user_id):
        return await self.repository.get_user(user_id=user_id)

    async def get_all_users(self):
        return await self.repository.get_all()

    async def get_all_doctors(self):
        return await self.repository.get_all_doctors()

    async def get_doctor(self, doctor_id: int):
        return await self.repository.get_doctor(user_id=doctor_id)

    async def edit_user(self, user_id: int, data: dict):
        return await self.repository.update_one(id_=user_id, **data)

    async def delete_user(self, user_id: int):

