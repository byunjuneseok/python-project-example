from sqlalchemy.exc import DatabaseError

from infra.exceptions.infra_exception import InfraException


class MySQLErrorException(InfraException):
    def __init__(self, err: DatabaseError):
        super().__init__(err)
        self.exec = err
