from dataclasses import dataclass
from typing import List

from geocube import entities
from geocube.pb import operations_pb2


@dataclass
class Dataset:
    container_subdir: str
    record_id: str
    instance_id: str
    bands: List[int]
    dformat: entities.DataFormat
    min_out: float
    max_out: float
    exponent: float

    def __post_init__(self):
        if len(self.bands) == 0:
            raise ValueError("Bands must not be empty")

    def to_pb(self) -> operations_pb2.Dataset:
        pbd = operations_pb2.Dataset(
            record_id=self.record_id,
            instance_id=self.instance_id,
            container_subdir=self.container_subdir,
            dformat=self.dformat.to_pb(),
            real_min_value=self.min_out,
            real_max_value=self.max_out,
            exponent=self.exponent,
            bands=self.bands)
        return pbd


@dataclass
class Container:
    uri: str
    managed: bool
    datasets: List[Dataset]

    @classmethod
    def new(cls, uri: str, record_id: str, instance_id: str, bands: List[int], dformat: entities.DataFormat,
            min_out: float, max_out: float, exponent: float = 1, container_subdir: str = "", managed: bool = False):
        """ Quickly define a container with one dataset """
        d = Dataset(record_id=record_id, instance_id=instance_id, bands=bands,
                    dformat=entities.DataFormat.from_user(dformat), min_out=min_out, max_out=max_out,
                    exponent=exponent, container_subdir=container_subdir)
        return cls(uri=uri, datasets=[d], managed=managed)
