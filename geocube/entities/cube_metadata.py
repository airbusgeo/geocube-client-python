from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, List, Set

import affine

from geocube import entities
from geocube.pb import datasetMeta_pb2, catalog_pb2


@dataclass
class SliceMetadata:
    grouped_records: entities.GroupedRecords
    metadata: List[datasetMeta_pb2.InternalMeta]
    bytes: int

    @property
    def record(self) -> entities.Record:
        assert len(self.grouped_records) == 1,\
            "This slice is the result of the fusion of several records. Call self.grouped_records"
        return self.grouped_records[0]

    @property
    def min_date(self) -> datetime:
        return min(r.datetime for r in self.grouped_records)

    @property
    def max_date(self) -> datetime:
        return max(r.datetime for r in self.grouped_records)

    @property
    def containers(self) -> Set[str]:
        return {m.container_uri for m in self.metadata}


@dataclass
class CubeMetadata:
    slices: List[SliceMetadata]

    crs: str
    transform: affine.Affine
    shape: Tuple[int, int]

    dformat: entities.DataFormat
    resampling_alg: entities.Resampling

    @classmethod
    def from_pb(cls, pb: catalog_pb2.GetCubeResponseHeader):
        return cls(
            slices=[],
            crs=pb.crs,
            transform=affine.Affine.from_gdal(
                pb.geotransform.a, pb.geotransform.b, pb.geotransform.c,
                pb.geotransform.d, pb.geotransform.e, pb.geotransform.f,
            ),
            shape=(0, 0),
            dformat=entities.DataFormat.from_pb(pb.ref_dformat),
            resampling_alg=entities.pb_resampling[pb.resampling_alg]
        )

    def info(self, verbose=True):
        files = set()
        datasets = 0
        for s in self.slices:
            files = files.union(s.containers)
            datasets += len(s.metadata)
        containers = len(files)
        images = len(self.slices)
        temporal_fragmentation = 0 if images <= 1 else (containers-1)/(datasets-1)
        spatial_fragmentation = 0 if datasets <= 1 else 1-images/datasets
        if verbose:
            print(f"{datasets} dataset(s) in {containers} container(s) for {images} image(s)\n"
                  f" - temporal fragmentation: {100*temporal_fragmentation:.0f}%\n"
                  f" - spatial fragmentation: {100*spatial_fragmentation:.0f}%\n")
        return {"datasets": datasets,
                "containers": containers,
                "images": images,
                "temporal_fragmentation": temporal_fragmentation,
                "spatial_fragmentation": spatial_fragmentation}
