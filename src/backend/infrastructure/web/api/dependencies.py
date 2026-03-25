from dependency_injector.wiring import Provide, inject
from domain.entities.user import UserEntity
from domain.services.auth import AuthServiceInterface
from domain.services.user import UserServiceInterface
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from infrastructure.config import app_settings
from infrastructure.container import Container
from starlette import status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{app_settings.API_V1_STR}/auth/token")


@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthServiceInterface = Depends(Provide[Container.services.auth_service]),
    user_service: UserServiceInterface = Depends(Provide[Container.services.user_service]),
) -> UserEntity:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = auth_service.decode_token(token)
    if username is None:
        raise credentials_exception

    user = await user_service.get_by_username(username)
    if user is None:
        raise credentials_exception

    return user
