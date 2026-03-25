from common.exceptions import TaskNotFoundException
from domain.entities.task import CreateTaskEntity, TaskEntity, TaskFilter, UpdateTaskEntity
from domain.services.task import TaskServiceInterface


class TaskService(TaskServiceInterface):
    def _invalidate_user_cache(self, user_id: int) -> None:
        keys_to_delete = [key for key in self.cache if str(key).startswith(f"top_tasks_{user_id}_")]
        for key in keys_to_delete:
            self.cache.pop(key, None)

    async def create(self, user_id: int, data: CreateTaskEntity) -> TaskEntity:
        result = await self.repo.create(user_id, data)
        self._invalidate_user_cache(user_id)
        return result

    async def get_tasks(self, user_id: int, filters: TaskFilter, sort_field: str, sort_desc: bool) -> list[TaskEntity]:
        return await self.repo.get_tasks(user_id, filters, sort_field, sort_desc)

    async def get_top_priority(self, user_id: int, limit_n: int) -> list[TaskEntity]:
        cache_key = f"top_tasks_{user_id}_{limit_n}"

        if cache_key in self.cache:
            return self.cache[cache_key]

        result = await self.repo.get_top_priority(user_id, limit_n)

        self.cache[cache_key] = result
        return result

    async def update(self, task_id: int, user_id: int, data: UpdateTaskEntity) -> TaskEntity:
        result = await self.repo.update(task_id, user_id, data)
        if result:
            self._invalidate_user_cache(user_id)
            return result
        else:
            raise TaskNotFoundException()

    async def delete(self, task_id: int, user_id: int) -> bool:
        is_deleted = await self.repo.delete(task_id, user_id)
        if is_deleted:
            self._invalidate_user_cache(user_id)
        return is_deleted
