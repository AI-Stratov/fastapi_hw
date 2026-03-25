from domain.entities.task import CreateTaskEntity, TaskEntity, TaskFilter, UpdateTaskEntity
from domain.repositories.task import TaskRepositoryInterface
from infrastructure.psql.models.task import TaskModel
from sqlalchemy import desc, or_, select


class TaskRepository(TaskRepositoryInterface):
    async def create(self, user_id: int, data: CreateTaskEntity) -> TaskEntity:
        async with self.session_factory() as session:
            db_obj = TaskModel(**data.model_dump(), user_id=user_id)
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return TaskEntity.model_validate(db_obj)

    async def get_by_id(self, task_id: int, user_id: int) -> TaskEntity | None:
        async with self.session_factory() as session:
            query = select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == user_id)
            result = await session.execute(query)
            db_obj = result.scalar_one_or_none()

            return TaskEntity.model_validate(db_obj) if db_obj else None

    async def get_tasks(
        self, user_id: int, filters: TaskFilter, sort_field: str = "created_at", sort_desc: bool = True
    ) -> list[TaskEntity]:
        async with self.session_factory() as session:
            query = select(TaskModel).where(TaskModel.user_id == user_id)

            if filters.search_query:
                search_term = f"%{filters.search_query}%"
                query = query.where(or_(TaskModel.title.ilike(search_term), TaskModel.description.ilike(search_term)))

            if filters.status:
                query = query.where(TaskModel.status == filters.status)

            sort_column = getattr(TaskModel, sort_field, TaskModel.created_at)
            query = query.order_by(sort_column.desc() if sort_desc else sort_column.asc())

            result = await session.execute(query)
            return [TaskEntity.model_validate(obj) for obj in result.scalars().all()]

    async def get_top_priority(self, user_id: int, limit_n: int = 5) -> list[TaskEntity]:
        async with self.session_factory() as session:
            query = (
                select(TaskModel).where(TaskModel.user_id == user_id).order_by(desc(TaskModel.priority)).limit(limit_n)
            )
            result = await session.execute(query)
            return [TaskEntity.model_validate(obj) for obj in result.scalars().all()]

    async def update(self, task_id: int, user_id: int, data: UpdateTaskEntity) -> TaskEntity | None:
        async with self.session_factory() as session:
            query = select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == user_id)
            result = await session.execute(query)
            db_obj = result.scalar_one_or_none()

            if not db_obj:
                return None

            update_data = data.model_dump(exclude_none=True)
            for key, value in update_data.items():
                setattr(db_obj, key, value)

            await session.commit()
            await session.refresh(db_obj)
            return TaskEntity.model_validate(db_obj)

    async def delete(self, task_id: int, user_id: int) -> bool:
        async with self.session_factory() as session:
            query = select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == user_id)
            result = await session.execute(query)
            db_obj = result.scalar_one_or_none()

            if not db_obj:
                return False

            await session.delete(db_obj)
            await session.commit()
            return True
