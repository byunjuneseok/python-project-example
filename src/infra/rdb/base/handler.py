from functools import wraps

from sqlalchemy.exc import DatabaseError

from infra.rdb.base.mysql_error_exception import MySQLErrorException


def _wrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DatabaseError as e:
            raise MySQLErrorException(e)

    return wrapper


class MySQLErrorHandler(type):
    def __new__(meta, classname, supers, classdict):
        for attr, attrval in classdict.items():
            if callable(attrval):
                classdict[attr] = _wrap(attrval)
        return type.__new__(meta, classname, supers, classdict)
