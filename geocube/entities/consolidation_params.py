import typing
from dataclasses import dataclass
from typing import Union

from geocube.pb import operations_pb2
from geocube import entities

@dataclass(frozen=True)
class ConsolidationParams:
    """
    Parameters of consolidation that describe the format of the consolidated datasets.
    It is linked to a variable, because ConsolidationParams are supposed to be the same for all datasets of
    all instances of the variable.

    Attributes:
        dformat:             dataformat of the consolidated data. See exponent for the mapping formula.
        exponent:            1: linear scaling
            otherwise: (RealMax - RealMin) * pow( (Value - Min) / (Max - Min), Exponent) + RealMin
        compression:         Define how the data is compressed at block level (see entities.Compression enum)
        creation_params:     Define creation options, including the compression options if compression==CUSTOM (see geocube documentation for supported options)
        resampling_alg:      Define how to resample the data during the consolidation (if a reprojection is needed or if
            the overviews are created)
    """
    dformat:             entities.DataFormat
    exponent:            float
    compression:         entities.Compression
    creation_params:     typing.Dict[str, str]
    resampling_alg:      entities.Resampling

    @classmethod
    def from_pb(cls, pb):
        return cls(
            dformat=entities.DataFormat.from_pb(pb.dformat),
            exponent=pb.exponent,
            compression=entities.pb_compression[pb.compression],
            creation_params=pb.creation_params,
            resampling_alg=entities.pb_resampling[pb.resampling_alg],
        )

    @classmethod
    def from_dict(cls, d: Union[dict, None]):
        if d is None:
            return None
        return cls(
            dformat=entities.DataFormat.from_dict(d["dformat"]),
            exponent=d["exponent"],
            compression=d["compression"],
            creation_params=d["creation_params"],
            resampling_alg=d["resampling_alg"],
        )

    def to_pb(self):
        return operations_pb2.ConsolidationParams(
            dformat=self.dformat.to_pb(),
            exponent=self.exponent,
            compression=typing.cast(int, self.compression.value)-1,
            creation_params=self.creation_params,
            resampling_alg=typing.cast(int, self.resampling_alg.value)-1)

    def __repr__(self):
        return "Consolidation Parameters\n" \
               "    dformat             {}\n" \
               "    exponent            {}\n" \
               "    compression         {}\n" \
               "    creation_params     {}\n" \
               "    resampling_alg      {}".format(self.dformat, self.exponent,
                                                   self.compression, self.creation_params, self.resampling_alg)
