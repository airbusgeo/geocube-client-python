import functools
from typing import Union

from geocube.pb import geocube_pb2_grpc as geocube_grpc, admin_pb2_grpc


class Stub:
    def __init__(self, stub: Union[geocube_grpc.GeocubeStub, admin_pb2_grpc.AdminStub], timeout: float = None):
        self._stub = stub
        self.timeout = timeout

    def __getattr__(self, item):
        if hasattr(self._stub, item):
            item = getattr(object.__getattribute__(self, "_stub"), item)
            if callable(item):
                return functools.partial(item, timeout=self.timeout)
            return item
        return object.__getattribute__(self, item)
