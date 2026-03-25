from http import HTTPStatus
from typing import Any

from common.exceptions import TaskNotFoundException
from common.logs import logger
from dependency_injector.wiring import Provide, inject
from domain.entities.rest import ErrorSchema, ResponseState, ResultResponse
from domain.entities.task import CreateTaskEntity, SortParams, TaskEntity, TaskFilter, UpdateTaskEntity
from domain.entities.user import UserEntity
from domain.services.task import TaskServiceInterface
from fastapi import APIRouter, Depends, HTTPException, Query
from infrastructure.container import Container
from infrastructure.web.api.dependencies import get_current_user

router = APIRouter()


@router.get(
    "/top/",
    summary="Топ-N приоритетных задач",
    response_model=ResultResponse[list[TaskEntity]],
    responses={
        HTTPStatus.OK: {"model": ResultResponse[list[TaskEntity]]},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": ErrorSchema},
    },
)
@inject
async def get_top_tasks(
    limit_n: int = Query(default=5, ge=1, le=50, description="Количество задач для выдачи"),
    current_user: UserEntity = Depends(get_current_user),
    service: TaskServiceInterface = Depends(Provide[Container.services.task_service]),
) -> Any:
    """
    Возвращает список самых приоритетных задач пользователя.

    - **limit_n**: ограничение количества (от 1 до 50).
    """
    try:
        result = await service.get_top_priority(current_user.id, limit_n)
        return ResultResponse(state=ResponseState.success, result=result)
    except Exception as e:
        logger.error(f"Error getting top tasks: {e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера") from e


@router.post(
    "/",
    summary="Создание задачи",
    status_code=HTTPStatus.CREATED,
    response_model=ResultResponse[TaskEntity],
    responses={
        HTTPStatus.CREATED: {"model": ResultResponse[TaskEntity]},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": ErrorSchema},
    },
)
@inject
async def create_task(
    data: CreateTaskEntity = Depends(CreateTaskEntity.as_form),
    current_user: UserEntity = Depends(get_current_user),
    service: TaskServiceInterface = Depends(Provide[Container.services.task_service]),
) -> Any:
    """
    Создает новую задачу для текущего пользователя.
    """
    try:
        result = await service.create(current_user.id, data)
        return ResultResponse(state=ResponseState.success, result=result)
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Ошибка при создании задачи") from e


@router.get(
    "/",
    summary="Получение списка задач",
    response_model=ResultResponse[list[TaskEntity]],
    responses={
        HTTPStatus.OK: {"model": ResultResponse[list[TaskEntity]]},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": ErrorSchema},
    },
)
@inject
async def get_tasks(
    filters: TaskFilter = Depends(TaskFilter.as_query),
    sort: SortParams = Depends(SortParams.as_query),
    current_user: UserEntity = Depends(get_current_user),
    service: TaskServiceInterface = Depends(Provide[Container.services.task_service]),
) -> Any:
    """
    Получение списка задач с поддержкой:

    - **Фильтрации**: по статусу или полнотекстовый поиск по заголовку.
    - **Сортировки**: по любому доступному полю.
    """
    try:
        result = await service.get_tasks(
            user_id=current_user.id, filters=filters, sort_field=sort.sort_field, sort_desc=sort.sort_desc
        )
        return ResultResponse(state=ResponseState.success, result=result)
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Ошибка при получении списка задач"
        ) from e


@router.patch(
    "/{id}/",
    summary="Обновление задачи",
    response_model=ResultResponse[TaskEntity],
    responses={
        HTTPStatus.OK: {"model": ResultResponse[TaskEntity]},
        HTTPStatus.NOT_FOUND: {"model": ErrorSchema},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": ErrorSchema},
    },
)
@inject
async def update_task(
    id: int,
    data: UpdateTaskEntity = Depends(UpdateTaskEntity.as_form),
    current_user: UserEntity = Depends(get_current_user),
    service: TaskServiceInterface = Depends(Provide[Container.services.task_service]),
) -> Any:
    """
    Частичное обновление задачи (PATCH).
    """
    try:
        result = await service.update(id, current_user.id, data)
        return ResultResponse(state=ResponseState.success, result=result)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Error updating task {id}: {e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Ошибка при обновлении задачи") from e


@router.delete(
    "/{id}/",
    summary="Удаление задачи",
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        HTTPStatus.NO_CONTENT: {"description": "Задача успешно удалена"},
        HTTPStatus.NOT_FOUND: {"model": ErrorSchema},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": ErrorSchema},
    },
)
@inject
async def delete_task(
    id: int,
    current_user: UserEntity = Depends(get_current_user),
    service: TaskServiceInterface = Depends(Provide[Container.services.task_service]),
) -> None:
    """
    Удаляет задачу по ID.
    """
    try:
        result = await service.delete(id, current_user.id)
        if not result:
            raise TaskNotFoundException()
        return None
    except TaskNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Error deleting task {id}: {e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Ошибка при удалении задачи") from e
