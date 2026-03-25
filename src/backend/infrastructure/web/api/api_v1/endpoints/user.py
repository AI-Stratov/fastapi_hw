from http import HTTPStatus
from typing import Any

from common.exceptions import InvalidCredentialsException, UserAlreadyExistsException
from common.logs import logger
from dependency_injector.wiring import Provide, inject
from domain.entities.rest import ErrorSchema, ResponseState, ResultResponse
from domain.entities.user import ChangePasswordEntity, UpdateUserEntity, UserEntity
from domain.services.user import UserServiceInterface
from fastapi import APIRouter, Depends, HTTPException
from infrastructure.container import Container
from infrastructure.web.api.dependencies import get_current_user

router = APIRouter()


@router.get(
    "/me/",
    response_model=ResultResponse[UserEntity],
    summary="Профиль текущего пользователя",
    responses={
        HTTPStatus.OK: {"model": ResultResponse[UserEntity]},
        HTTPStatus.UNAUTHORIZED: {"model": ErrorSchema},
    },
)
async def get_me(current_user: UserEntity = Depends(get_current_user)) -> Any:
    """
    Возвращает информацию о текущем авторизованном пользователе.
    Данные берутся из JWT токена и проверяются в БД.
    """
    return ResultResponse(state=ResponseState.success, result=current_user)


@router.patch(
    "/me/",
    response_model=ResultResponse[UserEntity],
    summary="Обновление профиля",
    responses={
        HTTPStatus.OK: {"model": ResultResponse[UserEntity]},
        HTTPStatus.BAD_REQUEST: {"model": ErrorSchema},
        HTTPStatus.UNAUTHORIZED: {"model": ErrorSchema},
    },
)
@inject
async def update_me(
    current_user: UserEntity = Depends(get_current_user),
    data: UpdateUserEntity = Depends(UpdateUserEntity.as_form),
    service: UserServiceInterface = Depends(Provide[Container.services.user_service]),
) -> Any:
    """
    Позволяет пользователю изменить свой username.
    """
    try:
        result = await service.update(current_user.id, data)
        return ResultResponse(state=ResponseState.success, result=result)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Error updating me: {e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера") from e


@router.put(
    "/me/password/",
    response_model=ResultResponse[str],
    summary="Изменение пароля пользователя",
)
@inject
async def change_password(
    current_user: UserEntity = Depends(get_current_user),
    data: ChangePasswordEntity = Depends(ChangePasswordEntity.as_form),
    service: UserServiceInterface = Depends(Provide[Container.services.user_service]),
) -> Any:
    """
    Позволяет авторизованному пользователю изменить свой пароль.
    """
    try:
        await service.change_password(current_user.id, current_user.username, data.old_password, data.new_password)

        return ResultResponse(state=ResponseState.success, result="Пароль успешно изменен")
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Неверный старый пароль") from e
    except Exception as e:
        logger.error(f"Error changing password: {e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Ошибка при смене пароля") from e
