from passlib.context import CryptContext


class PasswordHandler:
    def __init__(self, context: CryptContext):
        self.context = context

    def hash(self, password: str) -> str:
        return self.context.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self.context.verify(password, hashed_password)
