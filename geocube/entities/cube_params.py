from dataclasses import dataclass
from typing import List, Tuple, Dict, Union
import geopandas as gpd
from datetime import datetime

import affine

from geocube import entities

Tuple6Float = Tuple[float, float, float, float, float, float]


@dataclass
class CubeParams:
    _instance_id: str
    _records_id: Union[List[entities.GroupedRecordIds], None]

    tile: entities.Tile
    tags: Union[Dict[str, str], None]
    from_time: Union[datetime, None]
    to_time: Union[datetime, None]

    @classmethod
    def from_tags(cls, crs: str, transform: Union[affine.Affine, Tuple6Float],
                  shape: Tuple[int, int],
                  instance: Union[str, entities.VariableInstance, None],
                  tags: Dict[str, str], from_time: datetime = None, to_time: datetime = None):
        """
        Create a set of parameters to get a cube from record tags

        Parameters
        ----------
        crs: of the output images (images will be reprojected on the fly if necessary)
        transform: of the requested cube (images will be rescaled on the fly if necessary)
        shape: of the requested cube (@warning shape is the transpose of numpy shape)
        instance: of the requested data
        tags: of the records to be requested
        from_time: (optional) to filter the records
        to_time: (optional) to filter the records

        Returns
        -------
        A CubeParams to be passed as a parameter of a get_cube request
        """
        return cls.from_tile(entities.Tile.from_geotransform(transform, crs, shape), instance,
                             tags=tags, from_time=from_time, to_time=to_time)

    @classmethod
    def from_records(cls, records: List[entities.RecordIdentifiers],
                     crs: str, transform: Union[affine.Affine, Tuple6Float],
                     shape: Tuple[int, int],
                     instance: Union[str, entities.VariableInstance, None]):
        """
        Create a set of parameters to get a cube from a list of records

        Parameters
        ----------
        crs: of the output images (images will be reprojected on the fly if necessary)
        transform: of the requested cube (images will be rescaled on the fly if necessary)
        shape: of the requested cube (@warning shape is the transpose of numpy shape)
        instance: of the requested data
        records: to be retrieved

        Returns
        -------
        A CubeParams to be passed as a parameter of a get_cube request

        """
        return cls.from_tile(entities.Tile.from_geotransform(transform, crs, shape), instance, records=records)

    @classmethod
    def from_tile(cls, tile: entities.Tile,
                  instance: Union[str, entities.VariableInstance, None],
                  records: List[entities.RecordIdentifiers] = None,
                  tags: Dict[str, str] = None, from_time: datetime = None, to_time: datetime = None):
        """

        Parameters
        ----------
        tile: defining the Cube to be retrieved (images will be reprojected on the fly if necessary)
        instance: of the requested data
        records: (optional) to be retrieved
        tags: of the records to be requested
        from_time: (optional) to filter the records
        to_time: (optional) to filter the records

        Returns
        -------
        A CubeParams to be passed as a parameter of a get_cube request

        """
        return cls(tile=tile,
                   _instance_id=entities.get_id(instance) if instance else None,
                   _records_id=CubeParams._parse_grouped_record_ids(records),
                   tags=tags, from_time=from_time, to_time=to_time)

    @property
    def crs(self) -> str:
        return self.tile.crs

    @property
    def transform(self) -> affine.Affine:
        return self.tile.transform

    @property
    def shape(self) -> Tuple[int, int]:
        return self.tile.shape

    @property
    def records(self) -> List[entities.GroupedRecordIds]:
        return self._records_id

    @records.setter
    def records(self, records: List[entities.RecordIdentifiers]):
        self._records_id = CubeParams._parse_grouped_record_ids(records)

    @property
    def instance(self) -> str:
        return self._instance_id

    @instance.setter
    def instance(self, instance: Union[str, entities.VariableInstance]):
        self._instance_id = entities.get_id(instance)

    @staticmethod
    def _parse_grouped_record_ids(records: List[entities.RecordIdentifiers])\
            -> Union[List[entities.GroupedRecordIds], None]:
        return [CubeParams._parse_record_ids(rs) for rs in records] if records else None

    @staticmethod
    def _parse_record_ids(records: entities.RecordIdentifiers) -> List[str]:
        if isinstance(records, gpd.GeoDataFrame):
            return list(records['id'])
        return entities.get_ids(records)
