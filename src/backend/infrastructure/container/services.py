from application.auth_service import AuthService
from application.task_service import TaskService
from application.user_service import UserService
from dependency_injector import containers, providers
from infrastructure.config import auth_settings


class ServiceContainer(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()
    auth_service: providers.Factory[AuthService] = providers.Factory(
        AuthService,
        secret_key=auth_settings.SECRET_KEY,
        algorithm=auth_settings.ALGORITHM,
        expire_minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    user_service: providers.Factory[UserService] = providers.Factory(
        UserService,
        user_repo=repositories.user_repository,
        auth_service=auth_service,
    )
    task_service: providers.Factory[TaskService] = providers.Factory(
        TaskService,
        task_repo=repositories.task_repository,
        cache=repositories.task_cache,
    )
