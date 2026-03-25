from cachetools import TTLCache
from dependency_injector import containers, providers
from infrastructure.psql.repositories.task import TaskRepository
from infrastructure.psql.repositories.user import UserRepository


class RepositoryContainer(containers.DeclarativeContainer):
    db: providers.DependenciesContainer = providers.DependenciesContainer()
    user_repository: providers.Factory[UserRepository] = providers.Factory(
        UserRepository, session_factory=db.psql_db_client.provided.session
    )
    task_repository: providers.Factory[TaskRepository] = providers.Factory(
        TaskRepository, session_factory=db.psql_db_client.provided.session
    )
    task_cache = providers.Singleton(TTLCache, maxsize=100, ttl=300)
