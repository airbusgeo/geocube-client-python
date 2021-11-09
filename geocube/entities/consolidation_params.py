from dataclasses import dataclass

from geocube.pb import operations_pb2
from geocube import entities


@dataclass(frozen=True)
class ConsolidationParams:
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
