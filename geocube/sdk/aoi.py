from typing import Optional, Tuple, List

from shapely import geometry

import geocube
from geocube import entities


def tile_aoi(client: geocube.Client, aoi: geometry.MultiPolygon,
             resolution: Optional[float] = None,
             crs: Optional[str] = None, shape: Optional[Tuple[int, int]] = None,
             overlapping: int = None) -> List[geocube.entities.Tile]:
    tiles = client.tile_aoi(aoi, resolution=resolution, crs=crs, shape=(shape[0]-overlapping, shape[1]-overlapping))
    if overlapping != 0:
        for tile in tiles:
            tile.shape = (tile.shape[0] + overlapping, tile.shape[1] + overlapping)

    return tiles

