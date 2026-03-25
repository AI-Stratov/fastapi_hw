from http import HTTPStatus

from common.exceptions import InvalidCredentialsException, UserAlreadyExistsException
from common.logs import logger
from dependency_injector.wiring import Provide, inject
from domain.entities.auth import TokenEntity
from domain.entities.rest import ErrorSchema, ResponseState, ResultResponse
from domain.entities.user import CreateUserEntity, UserEntity
from domain.services.auth import AuthServiceInterface
from domain.services.user import UserServiceInterface
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from infrastructure.container import Container

router = APIRouter()


@router.post(
    "/register/",
    response_model=ResultResponse[UserEntity],
    status_code=HTTPStatus.CREATED,
    summary="Регистрация нового пользователя",
    responses={
        HTTPStatus.CREATED: {"model": ResultResponse[UserEntity]},
        HTTPStatus.BAD_REQUEST: {"model": ErrorSchema},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": ErrorSchema},
    },
)
@inject
async def register_user(
    data: CreateUserEntity = Depends(CreateUserEntity.as_form),
    user_service: UserServiceInterface = Depends(Provide[Container.services.user_service]),
):
    """
    Создает нового пользователя в системе.
    """
    try:
        user = await user_service.create(data)
        return ResultResponse(state=ResponseState.success, result=user)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Ошибка при регистрации") from e


@router.post(
    "/token/",
    response_model=TokenEntity,
    summary="Авторизация и получение JWT",
    responses={
        HTTPStatus.OK: {"model": TokenEntity},
        HTTPStatus.UNAUTHORIZED: {"model": ErrorSchema},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": ErrorSchema},
    },
)
@inject
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserServiceInterface = Depends(Provide[Container.services.user_service]),
    auth_service: AuthServiceInterface = Depends(Provide[Container.services.auth_service]),
):
    """
    Аутентификация через стандартный **OAuth2 Password Flow**.

    В Swagger используйте кнопку **Authorize** вверху страницы,
    чтобы автоматически подставлять токен во все защищенные запросы.
    """
    try:
        user = await user_service.authenticate(form_data.username, form_data.password)

        token = auth_service.create_access_token(user.username)

        return TokenEntity(access_token=token, token_type="bearer", username=user.username)
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Неверный логин или пароль") from e
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Ошибка авторизации") from e
