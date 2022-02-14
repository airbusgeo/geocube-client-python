from dataclasses import dataclass
from typing import List, Union

from geocube import entities
from geocube.pb import operations_pb2


@dataclass
class Dataset:
    """
    A dataset is the metadata to retrieve an image from a file (see entities.Container).
    It is defined by a record and the instance of a variable.
    A dataset defines:
      - Which band(s) are indexed (usually all the bands, but it can be a subset)
      - How to map the value of its pixels to the dataformat of the variable. In more details:
         . the dataformat of the dataset (dformat.[no_data, min, max]) that describes the pixel of the image
         . the mapping from each pixel to the data format of the variable (variable.dformat).
           This mapping is defined as [MinOut, MaxOut, Exponent].

    record_id:   id of the record describing the data-take
    instance_id: describing the data.
        @warning Must be an instance of Variable if one of bands, dformat, min_out, max_out is None
    bands:       subset of bands' container (start at 1) that maps to `variable.bands` (by default, all the bands)
    dformat:     describing the internal format (see entities.DataFormat.from_user())
    min_out:     (optional, default: instance.dformat.min_value, instance.dformat.dtype) maps dformat.min_value
    max_out:     (optional, default: instance.dformat.max_value, instance.dformat.dtype) maps dformat.max_value
    exponent:    (optional, default: 1) non-linear scaling between dformat.min_max_value to min_max_out.
    """
    record_id:   str
    instance_id: Union[str, entities.VariableInstance]
    container_subdir: str = ""
    bands:    List[int] = None
    dformat:  entities.DataFormat = None
    min_out:  float = None
    max_out:  float = None
    exponent: float = 1

    def __post_init__(self):
        if self.bands is None or self.min_out is None or self.max_out is None or self.dformat is None:
            assert isinstance(self.instance_id, entities.VariableInstance)
            if self.bands is None:
                self.bands = list(range(1, len(self.instance_id.bands)+1))
            if self.min_out is None:
                self.min_out = self.instance_id.dformat.min_value
            if self.max_out is None:
                self.max_out = self.instance_id.dformat.max_value
            if self.dformat is None:
                self.dformat = self.instance_id.dformat
        self.instance_id = entities.get_id(self.instance_id)
        self.record_id = entities.get_id(self.record_id)
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
    """
    Define a container of datasets.
    Usually a container is a file containing one dataset.
    But after a consolidation or if the container has several bands, it can contain several datasets.

    uri:      URI of the file
    managed:  True if the Geocube is responsible for the lifecycle of this file
    datasets: List of datasets of the container
    """
    uri: str
    managed: bool
    datasets: List[Dataset]
