from dependency_injector import containers, providers
from passlib.context import CryptContext

from cores.jwt.client import JWT
from cores.password.handler import PasswordHandler


class CoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    jwt: providers.Provider[JWT] = providers.Resource(
        JWT,
        secret_key=config.jwt.secret_key,
        algorithm="HS256",
        issuer=config.jwt.issuer,
        access_token_lifetime=config.jwt.access_token_lifetime,
        refresh_token_lifetime=config.jwt.refresh_token_lifetime,
    )
    password_context = providers.Singleton(CryptContext, schemes=["bcrypt"], deprecated="auto")
    password_handler = providers.Factory(PasswordHandler, context=password_context)
