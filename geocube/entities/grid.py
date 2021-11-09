from dataclasses import dataclass
from typing import Union, List

from shapely import geometry

from geocube.pb import layouts_pb2, records_pb2


@dataclass
class Cell:
    id: str
    crs: str
    coordinates: geometry.LinearRing

    def to_pb(self):
        return layouts_pb2.Cell(
            id=self.id,
            crs=self.crs,
            coordinates=records_pb2.LinearRing(
                points=[records_pb2.Coord(lon=x, lat=y) for x, y in zip(*self.coordinates.xy)]),
        )

    def from_pb(self):
        raise NotImplementedError

    @classmethod
    def from_geom(cls, id_: str, crs: str, geom: Union[geometry.Polygon, geometry.LinearRing]):
        return cls(id_, crs, geom.exterior if isinstance(geom, geometry.Polygon) else geom)


@dataclass
class Grid:
    name:        str
    description: str
    cells:       List[Cell]

    def to_pb(self):
        return layouts_pb2.Grid(
            name=self.name,
            description=self.description,
            cells=[cell.to_pb() for cell in self.cells]
        )

    @classmethod
    def from_pb(cls, pb_grid: layouts_pb2.Grid):
        return cls(
            name=pb_grid.name,
            description=pb_grid.description,
            cells=[Cell.from_pb(cell) for cell in pb_grid.cells]
        )

    def __str__(self):
        return "Grid '{}': {}".format(self.name, self.description)
