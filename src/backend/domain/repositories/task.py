from abc import ABC, abstractmethod
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager

from domain.entities.task import CreateTaskEntity, TaskEntity, TaskFilter, UpdateTaskEntity
from sqlalchemy.ext.asyncio import AsyncSession


class TaskRepositoryInterface(ABC):
    def __init__(
        self,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ):
        self.session_factory = session_factory

    @abstractmethod
    async def create(self, user_id: int, data: CreateTaskEntity) -> TaskEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, task_id: int, user_id: int) -> TaskEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_tasks(
        self, user_id: int, filters: TaskFilter, sort_field: str = "created_at", sort_desc: bool = True
    ) -> list[TaskEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_top_priority(self, user_id: int, limit_n: int = 5) -> list[TaskEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, task_id: int, user_id: int, data: UpdateTaskEntity) -> TaskEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, task_id: int, user_id: int) -> bool:
        raise NotImplementedError
