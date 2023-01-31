from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Union

from geocube import Client, Downloader


@dataclass
class ConnectionParams:
    """
    Defines the parameters to connect to a Geocube and, optionally, a Downloader.
    ConnectionParams is picklable (client and downloader are not).
    >>> cp = ConnectionParams("127.0.0.1:8080")
    >>> local_client = cp.new_client()
    >>> cp = ConnectionParams("geocube-server.com", True, "[API_KEY]", downloader=ConnectionParams("127.0.0.1:8080"))
    >>> distant_client = cp.new_client()
    >>> local_downloader  = cp.new_downloader()
    >>> import pickle
    >>> does_not_raise_error = pickle.loads(pickle.dumps(cp))
    """
    uri:     str
    secure:  bool = False
    api_key: str = ""
    verbose: bool = False

    downloader: Union[str, ConnectionParams] = None

    def __post_init__(self):
        if isinstance(self.downloader, str):
            self.downloader = ConnectionParams(self.downloader)

    def new_client(self, with_downloader=True) -> Client:
        """
        Create a new client connected to the geocube, using the ConnectionParams
        Use `with_downloader` to automatically use the downloader (defined by `self.downloader`) to the client
        """
        client = Client(**self.__as_dict())
        if with_downloader:
            client.use_downloader(self.new_downloader())
        return client

    def use_downloader(self, params: ConnectionParams):
        """ Defines the ConnectionParams of a downloader service """
        self.downloader = params

    def new_downloader(self) -> Union[Downloader, None]:
        """ Create a new downloader connected to the uri, using the ConnectionParams `self.downloader` """
        if self.downloader is not None:
            return Downloader(**self.downloader.__as_dict())
        return None

    def __as_dict(self):
        d = asdict(self)
        del d['downloader']
        return d
