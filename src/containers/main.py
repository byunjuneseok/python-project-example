from dependency_injector import containers, providers

from containers.core import CoreContainer
from containers.infra import InfraContainer
from containers.system import SystemContainer
from domains.user.services.user_my_service import UserMyService
from domains.user.services.user_service import UserService


class MainContainer(containers.DeclarativeContainer):
    # configurations
    wiring_config = containers.WiringConfiguration(
        packages=["applications", "contexts"]
    )
    config = providers.Configuration(yaml_files=["config.yml"])

    core = providers.Container(CoreContainer, config=config.core)
    system = providers.Container(SystemContainer, config=config.system)
    infra = providers.Container(InfraContainer, config=config.infra)

    # domains
    user_service = providers.Factory(
        UserService,
        user_repository=infra.user_repository,
        password_handler=core.password_handler,
    )
    user_my_service = providers.Factory(
        UserMyService,
        user_repository=infra.user_repository,
    )
