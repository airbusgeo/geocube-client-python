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

    @classmethod
    def from_rpc(cls, e: grpc.RpcError, func_name: str = ""):
        if isinstance(e, grpc.Call):
            return cls(func_name, e.code().name, e.details())
        return cls(func_name, grpc.StatusCode.INTERNAL.name, f"{e}")

    def __str__(self):
        return "Error {} [{}]: {}".format(self.func, self.codename, self.details)

    def __reduce__(self):
        return GeocubeError, (self.func, self.codename, self.details)

    def is_already_exists(self) -> bool:
        return self.codename == grpc.StatusCode.ALREADY_EXISTS.name

    def is_not_found(self) -> bool:
        return self.codename == grpc.StatusCode.NOT_FOUND.name

    def is_not_valid(self) -> bool:
        return self.codename == grpc.StatusCode.INVALID_ARGUMENT.name


def catch_rpc_error(func):
    @wraps(func)
    def wrapper(c, *args, **kwargs):
        try:
            if hasattr(c, "is_pid_ok") and not c.is_pid_ok():
                logging.warning("Close the client before using it in another thread.")
            return func(c, *args, **kwargs)
        except grpc.RpcError as e:
            raise GeocubeError.from_rpc(e, func.__name__)
        except ValueError as e:
            if "Channel closed due to fork" in str(e):
                logging.warning("Channel closed due to fork. Close the client before using it in another thread.")
            raise e
    return wrapper
