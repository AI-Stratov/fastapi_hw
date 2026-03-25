from domain.entities.user import CreateUserEntity, UpdateUserEntity, UserAuthEntity, UserEntity
from domain.repositories.user import UserRepositoryInterface
from infrastructure.psql.models.user import UserModel
from sqlalchemy import delete, select, update


class UserRepository(UserRepositoryInterface):
    async def create(self, data: CreateUserEntity) -> UserEntity:
        async with self.session_factory() as session:
            db_obj = UserModel(**data.model_dump())
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return UserEntity.model_validate(db_obj)

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        async with self.session_factory() as session:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)
            db_obj = result.scalar_one_or_none()

            return UserEntity.model_validate(db_obj) if db_obj else None

    async def get_by_username(self, username: str) -> UserEntity | None:
        async with self.session_factory() as session:
            query = select(UserModel).where(UserModel.username == username)
            result = await session.execute(query)
            db_obj = result.scalar_one_or_none()

            return UserEntity.model_validate(db_obj) if db_obj else None

    async def get_user_for_auth(self, username: str) -> UserAuthEntity | None:
        async with self.session_factory() as session:
            query = select(UserModel).where(UserModel.username == username)
            result = await session.execute(query)
            db_obj = result.scalar_one_or_none()
            return UserAuthEntity.model_validate(db_obj) if db_obj else None

    async def update(self, user_id: int, data: UpdateUserEntity) -> UserEntity | None:
        async with self.session_factory() as session:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)
            db_obj = result.scalar_one_or_none()

            if not db_obj:
                return None

            update_data = data.model_dump(exclude_none=True)
            for key, value in update_data.items():
                setattr(db_obj, key, value)

            await session.commit()
            await session.refresh(db_obj)
            return UserEntity.model_validate(db_obj)

    async def change_password(self, user_id: int, hashed_password: str) -> bool:
        async with self.session_factory() as session:
            query = update(UserModel).where(UserModel.id == user_id).values(password=hashed_password)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    async def delete(self, user_id: int) -> bool:
        async with self.session_factory() as session:
            query = delete(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0
