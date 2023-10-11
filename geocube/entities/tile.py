from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple, Union, List

import affine
from shapely import geometry
import pandas as pd
import geopandas as gpd

from geocube import entities, utils
from geocube.pb import layouts_pb2


def geo_transform(offset_x: float, offset_y: float, scale: Union[float, Tuple[float, float]]) -> affine.Affine:
    """ Return a geo_transform (if scale is a float: north-up convention)"""
    if isinstance(scale, tuple):
        return affine.Affine.translation(offset_x, offset_y) * affine.Affine.scale(scale[0], scale[1])
    return affine.Affine.translation(offset_x, offset_y) * affine.Affine.scale(scale, -scale)


def crs_to_str(crs: Union[str, int]) -> str:
    """
    Return a string representation of a crs
    Args:
        crs: an epsg number, a string or a class that support __str__() (e.g. pyproj.CRS)

    Returns:
        a string representation of the crs
    """
    if isinstance(crs, int):
        return f"epsg:{crs}"
    return str(crs)


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
    def from_geotransform(cls, transform: Union[affine.Affine, Tuple[float, float, float, float, float, float]],
                          crs: Union[str, int], shape: Tuple[int, int]) -> Tile:
        """
        Create a tile from a geotransform, a crs and a shape
        Args:
            transform: geotransform from pixel coordinates to CRS.
            crs: Coordinate Reference System of the tile
            shape: shape of the tile (in pixel) (@warning shape is the transpose of numpy shape)

        Returns:
            A new tile
        """
        return cls(crs_to_str(crs), Tile._parse_geotransform(transform), shape)

    @classmethod
    def from_record(cls, record: entities.Record, crs: Union[str, int], resolution: float) -> Tile:
        """ Create a tile that cover the record in the crs at a given resolution
        Warning: record.aoi must be loaded (with client.load_aoi())
        Warning: Check the `result.shape` as the size might be huge !
        Warning: the aoi is converted to the crs, but it might be imprecise at the borders

        Args:
            record:
            crs: Coordinate Reference System of the tile
            resolution: resolution of the pixel in the CRS

        Returns:
            A new tile
        """
        return Tile.from_aoi(record.aoi, crs, resolution)

    @classmethod
    def from_bbox(cls, bbox: Tuple[float, float, float, float], crs: Union[str, int],
                  resolution: Union[float, Tuple[float, float]]) -> Tile:
        """
        Create a tile from a bbox, a crs and a resolution
        Args:
            bbox : (x1, y1, x2, y2) in crs coordinates
            crs : (Coordinate Reference System) of the tile
            resolution : of the pixel in the CRS

        Returns:
            A new tile
        """
        rx, ry = resolution if isinstance(resolution, tuple) else (resolution, -resolution)
        x1, y1, x2, y2 = bbox
        if math.copysign(1, rx)*(x2-x1) < 0:
            x1, x2 = x2, x1
        if math.copysign(1, ry)*(y2-y1) < 0:
            y1, y2 = y2, y1
        transform = geo_transform(x1, y1, resolution)
        sx, sy = (~transform) * (x2, y2)
        return cls(crs_to_str(crs), transform, (math.ceil(sx), math.ceil(sy)))

    @classmethod
    def from_aoi(cls, aoi: geometry.MultiPolygon, crs: Union[str, int],
                 resolution: Union[float, Tuple[float, float]]) -> Tile:
        """

        Args:
            aoi : multipolygon in 4326 coordinates
            crs : (Coordinate Reference System) of the tile
            resolution : of the pixel in the CRS

        Returns:
            A new tile
        """
        return Tile.from_bbox(gpd.GeoSeries(aoi, crs=4326).to_crs(crs).total_bounds, crs=crs, resolution=resolution)

    def __str__(self):
        return "Tile {}\n" \
               "    transform: ({}, {} {}, {}, {} {})\n" \
               "    bounds:    {} {}\n" \
               "    shape:     {} \n" \
               "    crs:       {}\n".format(self.shape,
                                            self.transform.c, self.transform.a, self.transform.b,
                                            self.transform.f, self.transform.d, self.transform.e,
                                            self.transform*(0, 0), self.transform*self.shape,
                                            self.shape, self.crs)

    def __repr__(self):
        return self.__str__()

    def geoseries(self) -> gpd.GeoSeries:
        x1, y1 = self.transform*(0, 0)
        x2, y2 = self.transform*self.shape
        p = geometry.Polygon([[x1, y1], [x1, y2], [x2, y2], [x2, y1], [x1, y1]])
        return gpd.GeoSeries(p, crs=self.crs)

    def geometry(self, to_crs: Union[str, int] = None):
        gs = self.geoseries()
        if to_crs is not None:
            gs = gs.to_crs(crs_to_str(to_crs))
        return gs.iloc[0]

    def reshape(self, i1, j1, i2, j2) -> entities.Tile:
        """ Create a new Tile using the coordinate pixels
         @warning inverse of numpy coordinates """
        return Tile.from_bbox(self.transform*(i1, j1) + self.transform*(i2, j2),
                              self.crs, resolution=(self.transform.a, self.transform.e))

    @staticmethod
    def _parse_geotransform(transform: Union[affine.Affine, Tuple[float, float, float, float, float, float]]) \
            -> affine.Affine:
        if isinstance(transform, affine.Affine):
            return transform
        return affine.Affine.from_gdal(*transform)

    @staticmethod
    def to_geoseries(tiles: List[Tile]):
        """ return list of Tiles as geoseries """
        return gpd.GeoSeries(pd.concat([t.geoseries().to_crs("epsg:4326") for t in tiles]))

    @staticmethod
    def plot(tiles: List[Tile], **kwargs):
        """ kwargs: additional arguments for utils.plot_aoi """
        return utils.plot_aoi(Tile.to_geoseries(tiles), **kwargs)
