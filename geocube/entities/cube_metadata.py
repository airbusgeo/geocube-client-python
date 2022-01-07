from dataclasses import dataclass
from datetime import datetime
from typing import List

from geocube import entities
from geocube.pb import datasetMeta_pb2


@dataclass
class SliceMetadata:
    grouped_records: entities.GroupedRecords
    metadata: List[datasetMeta_pb2.InternalMeta]
    bytes: int

    @property
    def record(self) -> entities.Record:
        assert len(self.grouped_records) == 1, "This slice is defined by several records"
        return self.grouped_records[0]

    @property
    def min_date(self) -> datetime:
        return min(r.datetime for r in self.grouped_records)

    @property
    def max_date(self) -> datetime:
        return max(r.datetime for r in self.grouped_records)
