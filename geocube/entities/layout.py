import math
import pprint
from dataclasses import dataclass
from typing import Tuple, List, Dict, Union

from geocube.pb import layouts_pb2


MUCOGPattern = "Z=0>T>R>B;R>Z=1:>T>B"
COGPattern   = "R>Z=1:>T>B;R>Z=0>T>B"

@dataclass
class Layout:
    """
    Layout
    Attributes:
        overviews_min_size:  Maximum width or height of the smallest overview level. 0: No overview, -1: default=256.
        interlacing_pattern: To define how to interlace the records, the blocks, the bands and the overviews.
            See https://airbusgeo.github.io/geocube/user-guide/grpc/#geocube-ConsolidationParams
    """
    name:                str
    grid_flags:          List[str]
    grid_parameters:     Dict[str, str]
    block_shape:         Tuple[int, int]
    max_records:         int
    overviews_min_size:  int
    interlacing_pattern: str

    @classmethod
    def from_pb(cls, pb_layout: layouts_pb2.Layout):
        return cls(pb_layout.name, pb_layout.grid_flags, pb_layout.grid_parameters,
                   (pb_layout.block_x_size, pb_layout.block_y_size), pb_layout.max_records,
                   pb_layout.overviews_min_size, pb_layout.interlacing_pattern)

    def to_pb(self):
        return layouts_pb2.Layout(
            name=self.name,
            grid_flags=self.grid_flags,
            grid_parameters=self.grid_parameters,
            block_x_size=self.block_shape[0],
            block_y_size=self.block_shape[1],
            max_records=self.max_records,
            overviews_min_size=self.overviews_min_size,
            interlacing_pattern=self.interlacing_pattern
        )

    @classmethod
    def regular(cls, name: str, crs: str, cell_size: Union[int, Tuple[int, int]], resolution: float,
                block_size: int = 256, max_records: int = 1000,
                overviews_min_size: int = -1, interlacing_pattern=MUCOGPattern,
                origin: Tuple[float, float] = None):
        grid_parameters = {
            "grid": "regular",
            "crs": crs,
            "resolution": f"{resolution}",
        }
        if isinstance(cell_size, tuple):
            grid_parameters["cell_x_size"] = f"{cell_size[0]}"
            grid_parameters["cell_y_size"] = f"{cell_size[1]}"
        else:
            grid_parameters["cell_size"] = f"{cell_size}"

        if origin is not None:
            grid_parameters["ox"] = f"{origin[0]}"
            grid_parameters["oy"] = f"{origin[1]}"

        return cls(
            name=name,
            grid_parameters=grid_parameters,
            grid_flags=[],
            block_shape=(block_size, block_size),
            max_records=max_records,
            overviews_min_size=overviews_min_size,
            interlacing_pattern=interlacing_pattern
        )

    @classmethod
    def single_cell(cls, name: str, crs: str, resolution: int,
                    block_size: int = 256, max_records: int = 1000,
                    overviews_min_size: int = -1, interlacing_pattern=MUCOGPattern):
        grid_parameters = {
            "grid": "singlecell",
            "crs": crs,
            "resolution": f"{resolution}",
        }
        grid_flags = []

        return cls(
            name=name,
            grid_parameters=grid_parameters,
            grid_flags=grid_flags,
            block_shape=(block_size, block_size),
            max_records=max_records,
            overviews_min_size=overviews_min_size,
            interlacing_pattern=interlacing_pattern
        )

    @classmethod
    def web_mercator(cls, name: str, z_level: int, cell_size: int = 4096, **kwargs):
        """ Define a regular layout using web-mercator projection at a given z_level """
        earth_perimeter = 2*6378137*math.pi
        ox, oy, resolution = -earth_perimeter/2, earth_perimeter/2, earth_perimeter/(256*(1 << z_level))
        return Layout.regular(name, "epsg:3857", cell_size=cell_size, resolution=resolution,
                              block_size=256, origin=(ox, oy), **kwargs)

    def __repr__(self):
        return f"Layout '{self.name}'"

    def __str__(self):
        return "Layout '{}'\n" \
               "    grid_flags\n{}\n" \
               "    grid_parameters\n{}\n" \
               "    block_shape         {}\n" \
               "    max_records         {}\n" \
               "    overview_min_size   {}\n" \
               "    interlacing_pattern {}\n".format(self.name, "      \n".join(self.grid_flags),
                                                     pprint.pformat(self.grid_parameters, indent=7, width=1),
                                                     self.block_shape, self.max_records,
                                                     self.overviews_min_size, self.interlacing_pattern)
