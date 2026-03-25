from common.exceptions import InvalidCredentialsException, UserAlreadyExistsException, UserNotFoundException
from domain.entities.user import CreateUserEntity, UpdateUserEntity, UserEntity
from domain.services.user import UserServiceInterface


class UserService(UserServiceInterface):
    async def authenticate(self, username: str, password: str) -> UserEntity:
        user = await self.repo.get_user_for_auth(username)

        if not user:
            raise InvalidCredentialsException()

        is_valid = await self.auth_service.verify_password(password, user.password)
        if not is_valid:
            raise InvalidCredentialsException()

        return user

    async def create(self, data: CreateUserEntity) -> UserEntity:
        existing_user = await self.repo.get_by_username(data.username)
        if existing_user:
            raise UserAlreadyExistsException()

        hashed_password = await self.auth_service.hash_password(data.password)
        data_to_save = CreateUserEntity(username=data.username, password=hashed_password)
        return await self.repo.create(data_to_save)

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        return await self.repo.get_by_id(user_id)

    async def get_by_username(self, username: str) -> UserEntity | None:
        return await self.repo.get_by_username(username)

    async def update(self, user_id: int, data: UpdateUserEntity) -> UserEntity | None:
        if data.username:
            existing_user = await self.repo.get_by_username(data.username)
            if existing_user and existing_user.id != user_id:
                raise UserAlreadyExistsException()

        return await self.repo.update(user_id, data)

    async def change_password(self, user_id: int, username: str, old_password: str, new_password: str) -> bool:
        user = await self.repo.get_user_for_auth(username)
        if not user:
            raise UserNotFoundException
        is_valid_password = await self.auth_service.verify_password(old_password, user.password)
        if not is_valid_password:
            raise InvalidCredentialsException()
        hashed_password = await self.auth_service.hash_password(new_password)
        return await self.repo.change_password(user_id, hashed_password)

    async def delete(self, user_id: int) -> bool:
        return await self.repo.delete(user_id)
