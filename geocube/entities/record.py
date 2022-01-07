from __future__ import annotations

import pprint
from datetime import datetime

from typing import Dict, List, Union
from dataclasses import dataclass

import geopandas as gpd
from shapely import geometry

from geocube import utils
from geocube.pb import records_pb2


def aoi_from_pb(geom: records_pb2.AOI) -> geometry.MultiPolygon:
    polygons = []

    for p in geom.polygons:
        polygon = []
        for lr in p.linearrings:
            linearring = []
            for pt in lr.points:
                linearring.append([pt.lon, pt.lat])
            polygon.append(linearring)
        if len(polygon) == 1:
            polygon.append([])
        polygons.append(polygon)
    return geometry.MultiPolygon(polygons)


def aoi_to_pb(aoi: Union[geometry.Polygon, geometry.MultiPolygon]) -> records_pb2.AOI:
    if aoi is None:
        return None

    if not (isinstance(aoi, geometry.Polygon) or isinstance(aoi, geometry.MultiPolygon)):
        raise ValueError("Geometry not supported")

    if isinstance(aoi, geometry.Polygon):
        return records_pb2.AOI(
            polygons=[records_pb2.Polygon(
                linearrings=[records_pb2.LinearRing(
                    points=[records_pb2.Coord(lon=coord[0], lat=coord[1]) for coord in lr.coords]
                    ) for lr in [aoi.exterior, *aoi.interiors]]
                )]
            )

    return records_pb2.AOI(
        polygons=[records_pb2.Polygon(
            linearrings=[records_pb2.LinearRing(
                points=[records_pb2.Coord(lon=coord[0], lat=coord[1]) for coord in lr.coords]
                ) for lr in [p.exterior, *p.interiors]]
            ) for p in list(aoi)]
        )


@dataclass
class Record:
    id:       str
    name:     str
    datetime: datetime
    tags:     Dict[str, str]
    aoi_id:   str

    _aoi:     geometry.MultiPolygon = geometry.MultiPolygon()

    @classmethod
    def from_pb(cls, pb: records_pb2.Record):
        return cls(
            id=pb.id,
            name=pb.name,
            tags={key: value for key, value in pb.tags.items()},
            datetime=pb.time.ToDatetime(),
            aoi_id=pb.aoi_id,
            _aoi=aoi_from_pb(pb.aoi)
        )

    @classmethod
    def from_geodataframe(cls, gdf: gpd.GeoDataFrame):
        return cls(
            id=gdf["id"].iloc[0],
            name=gdf["name"].iloc[0],
            tags={k: v for k, v in gdf["tags"].iloc[0]},
            datetime=gdf["datetime"].iloc[0],
            aoi_id=gdf["aoi_id"].iloc[0],
            _aoi=gdf.geometry.iloc[0]
        )

    def to_pb(self) -> records_pb2.Record:
        pb = records_pb2.Record(
            id=self.id,
            name=self.name,
            tags={key: value for key, value in self.tags.items()},
            aoi_id=self.aoi_id
        )
        pb.time.FromDatetime(self.datetime)
        return pb

    def geodataframe(self) -> gpd.GeoDataFrame:
        self._check_aoi()
        return gpd.GeoDataFrame(
            {
                "id": [self.id],
                "name": [self.name],
                "tags": [[(k, v) for k, v in self.tags.items()]],
                "datetime": [str(self.datetime)],
                "aoi_id": [self.aoi_id],
                "geometry": [self.aoi]
            },
            crs='epsg:4326'
        )

    @property
    @utils.catch_rpc_error
    def aoi(self) -> geometry.MultiPolygon:
        self._check_aoi()
        return self._aoi

    @aoi.setter
    def aoi(self, aoi: geometry.MultiPolygon):
        self._aoi = aoi

    def __repr__(self):
        return "Record {} ({})".format(self.name, self.id)

    def __str__(self):
        return "Record {} ({})\n" \
               "    datetime {}\n" \
               "    tags     \n{}\n"\
               "    aoi_id   {}\n".format(self.name, self.id, self.datetime,
                                          pprint.pformat(self.tags, indent=6, width=1), self.aoi_id) + \
               "    aoi      {}\n".format(self.aoi if not self._aoi.is_empty else "(not loaded)")

    @staticmethod
    def key_date(r: Record):
        return r.datetime.date()

    @staticmethod
    def group_by(records: List[Union[Record, GroupedRecords]], func_key) -> List[GroupedRecords]:
        """
        group_by groups the records of the list by the key provided by the func_key(Record)
        Returns a list of lists of records

        Parameters
        ----------
        records: list of records to group. If records is a list of list, records is flattened.
        func_key: function taking a record and returning a key (e.g. entities.Record.key_date, lambda r:r.datetime)

        Returns
        -------
        A list of grouped records (which is actually a list of records)
        """
        if isinstance(records[0], list):
            records = [r for rs in records for r in rs]
            return Record.group_by(records, func_key)

        dict_rs = {}
        for r in records:
            k = func_key(r)
            if k not in dict_rs:
                dict_rs[k] = [r]
            else:
                dict_rs[k].append(r)
        return list(dict_rs.values())

    @staticmethod
    def list_to_geodataframe(records: List[Record]) -> gpd.GeoDataFrame:
        return gpd.GeoDataFrame(
            {
                "id": [r.id for r in records],
                "name": [r.name for r in records],
                "tags": [[(k, v) for k, v in r.tags.items()] for r in records],
                "datetime": [str(r.datetime) for r in records],
                "aoi_id": [r.aoi_id for r in records],
                "geometry": [r.aoi for r in records],
            },
            crs='epsg:4326'
        )

    def _check_aoi(self, raise_if_empty=True) -> bool:
        if self._aoi.is_empty:
            if raise_if_empty:
                raise ReferenceError("AOI is not loaded. Call 'client.load_aoi(record)'")
            return False
        return True


GroupedRecords = List[Record]
GroupedRecordIds = List[str]
RecordIdentifiers = Union[str, Record, GroupedRecordIds, GroupedRecords, gpd.GeoDataFrame]
