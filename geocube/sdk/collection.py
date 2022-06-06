import copy
from dataclasses import dataclass
from typing import List, Tuple, Dict, Union, Any
from datetime import datetime

from shapely import geometry

import geocube
from geocube import entities

Tuple6Float = Tuple[float, float, float, float, float, float]


@dataclass
class Collection:
    """
    A collection of images is basically defined by
    - a collection of records
    - a collection of variable instances
    - a regular grid

    But it can be defined in several ways, for example, with an aoi, tags, a time interval, a layout...

    The fields available to define a Collection are:
    - `aoi` in geographic coordinates of the zone
    - `records`
    - `tags` of the records
    - `from_time`, `to_time` of the interval
    - `instances` of the variables
    - `layout` of the grid (may include internal layout to optimize the retrieval)
    """
    aoi: geometry.MultiPolygon = None
    records: Union[entities.RecordIdentifiers, None] = None
    tags: Union[Dict[str, str], None] = None
    from_time: Union[datetime, None] = None
    to_time: Union[datetime, None] = None

    instances: Union[List[entities.VariableInstance], List[str], None] = None

    layout: entities.Layout = None

    group_key_func: entities.GroupByKeyFunc = None  # Not fully supported yet

    _cube_params: entities.CubeParams = None
    _record_keys: List[Any] = None
    _record_ids: List[entities.GroupedRecordIds] = None

    @classmethod
    def from_tile(cls, tile: entities.Tile, **kwargs):
        """
        Define a collection from a tile

        Args:
            tile: defining the Cube to be retrieved (images will be reprojected on the fly if necessary)
            kwargs: all other params to define the collection

        Returns:
            A Collection defining images

        """
        cp_kwargs = {k: v for k, v in kwargs.items() if k in entities.CubeParams.from_tile.__code__.co_varnames}
        return cls(_cube_params=entities.CubeParams.from_tile(tile, instance=None, **cp_kwargs), **kwargs)

    def cube_params(self, client: geocube.Client, instance_id: Union[str, entities.VariableInstance]):
        assert self._cube_params is not None, "unimplemented error"
        cp = copy.deepcopy(self._cube_params)
        cp.instance = instance_id
        return cp

    def record_keys(self, client: geocube.Client) -> List[Any]:
        if self._record_keys is None:
            self._load_records(client)

        return self._record_keys

    def record_ids(self, client: geocube.Client) -> List[entities.GroupedRecordIds]:
        if self._record_ids is None:
            self._load_records(client)

        return self._record_ids

    def variables(self, client) -> List[entities.VariableInstance]:
        self.instances = [instance_id if isinstance(instance_id, entities.VariableInstance)
                          else client.variable(instance_id=instance_id)
                          for instance_id in self.instances]
        return self.instances

    # def record_ids(self, client: geocube.Client):
    #     """ record_ids from metadata """
    #     if self._record_ids is None:
    #         self._get_records(client)
    #         if isinstance(self.records, (str, entities.Record)):
    #             self._record_ids = [[entities.get_id(self.records)]]
    #         else:
    #             self._record_ids = [entities.get_ids(rid) for rid in self.records]
    #     return self._record_ids
#
    # def _get_records(self, client: geocube.Client) -> List[entities.GroupedRecords]:
    #     """ Records can be retrieved from
    #     - aoi, tags, from_time, to_time
    #     - get_cube_metadata
    #     """
    #     assert self.tags is not None or self.aoi is not None,\
    #         "collection invalid parameters: tags or aoi must be defined"
    #     records = client.list_records(tags=self.tags,
    #                                   aoi=self.aoi,
    #                                   from_time=self.from_time,
    #                                   to_time=self.to_time,
    #                                   limit=0)
    #     return entities.Record.group_by(records, lambda r: r.datetime)

    def _load_records(self, client: geocube.Client):
        # Load keys
        records = {}
        for instance_id in self.instances:
            metadata = client.get_cube_metadata(self.cube_params(client, instance_id))
            for sl in metadata.slices:
                key = sl.record.datetime if len(sl.grouped_records) == 1 \
                    else self.group_key_func(sl.grouped_records[0])
                ids = entities.get_ids(sl.grouped_records)
                if key in records:
                    records[key] = records[key].union(ids)
                else:
                    records[key] = set(ids)
        records = dict(sorted(records.items()))
        self._record_keys = list(records.keys())
        self._record_ids = list(records.values())

