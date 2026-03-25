from abc import ABC, abstractmethod

from cachetools import Cache
from domain.entities.task import CreateTaskEntity, TaskEntity, TaskFilter, UpdateTaskEntity
from domain.repositories.task import TaskRepositoryInterface


class TaskServiceInterface(ABC):
    def __init__(self, task_repo: TaskRepositoryInterface, cache: Cache):
        self.repo = task_repo
        self.cache = cache

    @abstractmethod
    async def create(self, user_id: int, data: CreateTaskEntity) -> TaskEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_tasks(self, user_id: int, filters: TaskFilter, sort_field: str, sort_desc: bool) -> list[TaskEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_top_priority(self, user_id: int, limit_n: int) -> list[TaskEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, task_id: int, user_id: int, data: UpdateTaskEntity) -> TaskEntity:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, task_id: int, user_id: int) -> bool:
        raise NotImplementedError
