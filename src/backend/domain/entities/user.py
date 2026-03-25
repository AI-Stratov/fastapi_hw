from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserEntity(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateUserEntity(UserBase):
    password: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(
            ...,
            title="Имя пользователя",
            description="Уникальное имя (используется для входа)",
            examples=["user"],
        ),
        password: str = Form(
            ...,
            title="Пароль",
            description="Будет захеширован перед сохранением.",
            examples=["temp"],
        ),
    ) -> "CreateUserEntity":
        return cls(username=username, password=password)


class UpdateUserEntity(BaseModel):
    username: str | None = None

    @classmethod
    def as_form(
        cls,
        username: str | None = Form(None, title="Имя пользователя", description="Имя пользователя", examples=["user"]),
    ) -> "UpdateUserEntity":
        return cls(username=username)


class ChangePasswordEntity(BaseModel):
    old_password: str
    new_password: str

    @classmethod
    def as_form(
        cls,
        old_password: str = Form(..., title="Старый пароль", description="Текущий пароль", examples=["temp"]),
        new_password: str = Form(..., title="Новый пароль", description="Новый пароль", examples=["temp2"]),
    ) -> "ChangePasswordEntity":
        return cls(old_password=old_password, new_password=new_password)


class UserAuthEntity(UserEntity):
    password: str
