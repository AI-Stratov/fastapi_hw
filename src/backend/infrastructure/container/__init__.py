from dependency_injector import containers, providers

from .database import DatabaseContainer
from .repositories import RepositoryContainer
from .services import ServiceContainer


class Container(containers.DeclarativeContainer):
    db = providers.Container(DatabaseContainer)
    repositories = providers.Container(RepositoryContainer, db=db)
    services = providers.Container(ServiceContainer, repositories=repositories)


def init_container():
    container = Container()
    container.init_resources()
    return container
