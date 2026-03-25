from abc import ABC, abstractmethod

from passlib.context import CryptContext


class AuthServiceInterface(ABC):
    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @abstractmethod
    async def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create_access_token(self, username: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> str | None:
        raise NotImplementedError
