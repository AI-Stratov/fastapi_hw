import asyncio
from datetime import UTC, datetime, timedelta

from domain.services.auth import AuthServiceInterface
from jose import JWTError, jwt


class AuthService(AuthServiceInterface):
    async def hash_password(self, password: str) -> str:
        return await asyncio.to_thread(self.pwd_context.hash, password)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return await asyncio.to_thread(self.pwd_context.verify, plain_password, hashed_password)

    def create_access_token(self, username: str) -> str:
        expire = datetime.now(UTC) + timedelta(minutes=self.expire_minutes)
        to_encode = {"sub": username, "exp": expire}
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload.get("sub")
        except JWTError:
            return None
