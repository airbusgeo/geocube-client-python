from typing import Optional, Tuple, List, Union

from affine import Affine
from shapely import geometry

import geocube
from geocube import entities


def tile_aoi(client: geocube.Client, aoi: Union[geometry.Polygon, geometry.MultiPolygon],
             resolution: Optional[float] = None,
             crs: Optional[str] = None, shape: Optional[Union[int, Tuple[int, int]]] = None,
             overlap: int = None, center_overlap: bool = False) -> List[geocube.entities.Tile]:
    if isinstance(shape, int):
        shape = (shape, shape)
    tiles = client.tile_aoi(aoi, resolution=resolution, crs=crs, shape=(shape[0]-overlap, shape[1]-overlap))
    if overlap != 0:
        for tile in tiles:
            tile.shape = (tile.shape[0] + overlap, tile.shape[1] + overlap)
            if center_overlap:
                tile.transform *= Affine.translation(-overlap/2, -overlap/2)

    return tiles

