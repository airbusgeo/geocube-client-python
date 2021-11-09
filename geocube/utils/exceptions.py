import logging
import sys
from functools import wraps

import grpc


def my_exception_handler(type_, value, traceback):
    if type.__name__ != 'GeocubeError':
        sys.__excepthook__(type_, value, traceback)
    else:
        logging.error(value)


sys.excepthook = my_exception_handler


class GeocubeError(Exception):
    def __init__(self, func: str, codename: str, details: str):
        self.func = func
        self.codename = codename
        self.details = details
        super().__init__(self.__str__())

    def __str__(self):
        return "Error {} [{}]: {}".format(self.func, self.codename, self.details)

    def __reduce__(self):
        return GeocubeError, (self.func, self.codename, self.details)


def catch_rpc_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except grpc.RpcError as e:
            raise GeocubeError(func.__name__, e.code().name, e.details())
    return wrapper
