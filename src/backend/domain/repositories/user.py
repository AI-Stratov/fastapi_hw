from abc import ABC, abstractmethod
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager

from domain.entities.user import CreateUserEntity, UpdateUserEntity, UserAuthEntity, UserEntity
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepositoryInterface(ABC):
    def __init__(
        self,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ):
        self.session_factory = session_factory

    @abstractmethod
    async def create(self, data: CreateUserEntity) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_for_auth(self, username: str) -> UserAuthEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user_id: int, data: UpdateUserEntity) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def change_password(self, user_id: int, hashed_password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        raise NotImplementedError
