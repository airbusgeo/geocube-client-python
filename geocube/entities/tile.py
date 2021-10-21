from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple, Union, List

import affine
from shapely import geometry
import pandas as pd
import geopandas as gpd

from geocube import entities
from geocube.pb import layouts_pb2


def geo_transform(offset_x, offset_y, scale) -> affine.Affine:
    """ Return a geo_transform """
    return affine.Affine.translation(offset_x, offset_y) * affine.Affine.scale(scale, -scale)


@dataclass
class Tile:
    crs:       str
    transform: affine.Affine  # Pixel to crs
    shape:     Tuple[int, int]

    @classmethod
    def from_pb(cls, pb: layouts_pb2.Tile):
        return cls(pb.crs, affine.Affine(pb.transform.b, pb.transform.c, pb.transform.a,
                                         pb.transform.e, pb.transform.f, pb.transform.d),
                   shape=(int(pb.size_px.width), int(pb.size_px.height))
                   )

    @classmethod
    def from_geotransform(cls, crs: str,
                          transform: Union[affine.Affine, Tuple[float, float, float, float, float, float]],
                          shape: Tuple[int, int]):
        return cls(crs, Tile._parse_geotransform(transform), shape)

    @classmethod
    def from_record(cls, record: entities.Record, crs: str, resolution: float):
        """ Create a tile that cover the record in the crs at a given resolution
        Warning: record.aoi must be loaded (with client.load_aoi())
        Warning: Check the result.shape as the size might be really big !
        Warning: the aoi is converted to the crs but it might be imprecise at the borders
        """
        bounds = record.geodataframe().to_crs(crs).total_bounds
        return Tile.from_bbox(crs, bounds, resolution)

    @classmethod
    def from_bbox(cls, crs: str,
                  bbox: Tuple[float, float, float, float],
                  resolution: float):
        transform = geo_transform(bbox[0], bbox[3], resolution)
        sx, sy = (~transform) * (bbox[2], bbox[1])
        return cls(crs, transform, (math.ceil(sx), math.ceil(sy)))

    def __str__(self):
        return "Tile {}\n" \
               "    transform: ({}, {} {}, {}, {} {})\n" \
               "    bounds:    ({} {}) {}\n" \
               "    shape:     {} \n" \
               "    crs:       {}\n".format(self.shape,
                                            self.transform.c, self.transform.a, self.transform.b,
                                            self.transform.f, self.transform.d, self.transform.e,
                                            self.transform.c, self.transform.f, self.transform*self.shape,
                                            self.shape, self.crs)

    def __repr__(self):
        return self.__str__()

    def geoseries(self) -> gpd.GeoSeries:
        x1, y1 = self.transform*(0, 0)
        x2, y2 = self.transform*self.shape
        p = geometry.Polygon([[x1, y1], [x1, y2], [x2, y2], [x2, y1], [x1, y1]])
        return gpd.GeoSeries(p, crs=self.crs)

    def geometry(self, to_crs: str = None):
        gs = self.geoseries()
        if to_crs is not None:
            gs = gs.to_crs(to_crs)
        return gs.iloc[0]

    @staticmethod
    def _parse_geotransform(transform: Union[affine.Affine, Tuple[float, float, float, float, float, float]]) \
            -> affine.Affine:
        if isinstance(transform, affine.Affine):
            return transform
        return affine.Affine.from_gdal(*transform)

    @staticmethod
    def plot(tiles: List[Tile], world_path: str = gpd.datasets.get_path('naturalearth_lowres'), ax=None, margin_pc=5):
        if world_path is not None:
            base = gpd.read_file(world_path).plot(color='lightgrey', edgecolor='white', ax=ax)
        else:
            base = ax

        ts = gpd.GeoSeries(pd.concat([t.geoseries().to_crs("epsg:4326") for t in tiles]))
        ts.plot(ax=base, alpha=0.5, edgecolor='gray')
        bounds = ts.total_bounds
        margin = (margin_pc/100)*min(bounds[2] - bounds[0], bounds[3] - bounds[1])
        base.set_xlim(bounds[0]-margin, bounds[2]+margin)
        base.set_ylim(bounds[1]-margin, bounds[3]+margin)
        return base
