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
        dformat:            dataformat of the consolidated data. See exponent for the mapping formula.
        exponent:           1: linear scaling
            otherwise: (RealMax - RealMin) * pow( (Value - Min) / (Max - Min), Exponent) + RealMin
        compression:        Define how the data is compressed at block level (see entities.Compression enum)
        overviews_min_size: Maximum width or height of the smallest overview level. 0: No overview, -1: default=256.
        resampling_alg:     Define how to resample the data during the consolidation (if a reprojection is needed or if
            the overviews are created)
        bands_interleave:   If the variable is multibands, define whether the bands are interleaved
    """
    dformat:            entities.DataFormat
    exponent:           float
    compression:        entities.Compression
    overviews_min_size: int
    resampling_alg:     entities.Resampling
    bands_interleave:   bool

    @classmethod
    def from_pb(cls, pb):
        return cls(
            dformat=entities.DataFormat.from_pb(pb.dformat),
            exponent=pb.exponent,
            compression=entities.pb_compression[pb.compression],
            overviews_min_size=pb.overviews_min_size,
            resampling_alg=entities.pb_resampling[pb.resampling_alg],
            bands_interleave=pb.bands_interleave,
        )

    @classmethod
    def from_dict(cls, d: Union[dict, None]):
        if d is None:
            return None
        return cls(
            dformat=entities.DataFormat.from_dict(d["dformat"]),
            exponent=d["exponent"],
            compression=d["compression"],
            overviews_min_size=d["overviews_min_size"],
            resampling_alg=d["resampling_alg"],
            bands_interleave=d["bands_interleave"],
        )

    def to_pb(self):
        return operations_pb2.ConsolidationParams(
            dformat=self.dformat.to_pb(),
            exponent=self.exponent, bands_interleave=self.bands_interleave,
            compression=self.compression.value-1, overviews_min_size=self.overviews_min_size,
            resampling_alg=self.resampling_alg.value-1)

    def __repr__(self):
        return "Consolidation Parameters\n" \
               "    dformat            {}\n" \
               "    exponent           {}\n" \
               "    bands_interleave   {}\n" \
               "    compression        {}\n" \
               "    overviews_min_size {}\n" \
               "    resampling_alg     {}".format(self.dformat, self.exponent, self.bands_interleave, self.compression,
                                                  self.overviews_min_size, self.resampling_alg)
