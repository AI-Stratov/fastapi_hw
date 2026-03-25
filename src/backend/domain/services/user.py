from abc import ABC, abstractmethod

from domain.entities.user import CreateUserEntity, UpdateUserEntity, UserEntity
from domain.repositories.user import UserRepositoryInterface
from domain.services.auth import AuthServiceInterface


class UserServiceInterface(ABC):
    def __init__(self, user_repo: UserRepositoryInterface, auth_service: AuthServiceInterface):
        self.repo = user_repo
        self.auth_service = auth_service

    @abstractmethod
    async def authenticate(self, username: str, password: str) -> UserEntity:
        raise NotImplementedError

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
    async def update(self, user_id: int, data: UpdateUserEntity) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def change_password(self, user_id: int, username: str, old_password: str, new_password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        raise NotImplementedError
