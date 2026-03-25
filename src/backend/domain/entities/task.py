from datetime import datetime
from enum import StrEnum

from fastapi import Form, Query
from pydantic import BaseModel, ConfigDict, Field


class TaskStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    priority: int = Field(default=0, ge=0)


class TaskEntity(TaskBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateTaskEntity(TaskBase):
    @classmethod
    def as_form(
        cls,
        title: str = Form(
            ...,
            min_length=1,
            max_length=255,
            title="Название",
            description="Краткое название задачи",
            examples=["Купить молоко"],
        ),
        description: str | None = Form(
            None,
            title="Описание",
            description="Подробное описание задачи",
            examples=["Сходить в супермаркет вечером и купить пакет молока"],
        ),
        status: TaskStatus = Form(
            TaskStatus.PENDING, title="Статус", description="Текущий статус задачи", examples=[TaskStatus.PENDING]
        ),
        priority: int = Form(
            0,
            ge=0,
            title="Приоритет",
            description="Приоритет задачи (число >= 0). Чем выше число, тем важнее.",
            examples=[1],
        ),
    ) -> "CreateTaskEntity":
        return cls(title=title, description=description, status=status, priority=priority)


class UpdateTaskEntity(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: int | None = None

    @classmethod
    def as_form(
        cls,
        title: str | None = Form(
            None, min_length=1, max_length=255, title="Название", description="Новое название", examples=[""]
        ),
        description: str | None = Form(None, title="Описание", description="Новое описание", examples=[""]),
        status: TaskStatus | None = Form(None, title="Статус", description="Обновить статус"),
        priority: int | None = Form(None, ge=0, title="Приоритет", description="Обновить приоритет", examples=[""]),
    ) -> "UpdateTaskEntity":
        return cls(title=title, description=description, status=status, priority=priority)


class TaskFilter(BaseModel):
    search_query: str | None = None
    status: TaskStatus | None = None

    @classmethod
    def as_query(
        cls,
        search_query: str | None = Query(
            None, title="Поиск", description="Поиск по названию или описанию", examples=["молоко"]
        ),
        status: TaskStatus | None = Query(
            None, title="Статус", description="Фильтрация по статусу задачи", examples=[TaskStatus.COMPLETED]
        ),
    ) -> "TaskFilter":
        return cls(search_query=search_query, status=status)


class SortParams(BaseModel):
    sort_field: str = "created_at"
    sort_desc: bool = True

    @classmethod
    def as_query(
        cls,
        sort_field: str = Query(
            "created_at",
            title="Поле сортировки",
            description="Поле, по которому будет производиться сортировка (например: created_at, title, priority)",
            examples=["priority"],
        ),
        sort_desc: bool = Query(
            True,
            title="Порядок сортировки",
            description="Сортировка по убыванию (True) или по возрастанию (False)",
            examples=[True],
        ),
    ) -> "SortParams":
        return cls(sort_field=sort_field, sort_desc=sort_desc)
