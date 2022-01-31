import math
import pprint
from dataclasses import dataclass
from typing import Tuple, List, Dict, Union

from geocube.pb import layouts_pb2


@dataclass
class Layout:
    name:            str
    grid_flags:      List[str]
    grid_parameters: Dict[str, str]
    block_shape:     Tuple[int, int]
    max_records:     int

    @classmethod
    def from_pb(cls, pb_layout: layouts_pb2.Layout):
        return cls(pb_layout.name, pb_layout.grid_flags, pb_layout.grid_parameters,
                   (pb_layout.block_x_size, pb_layout.block_y_size), pb_layout.max_records)

    def to_pb(self):
        return layouts_pb2.Layout(
            name=self.name,
            grid_flags=self.grid_flags,
            grid_parameters=self.grid_parameters,
            block_x_size=self.block_shape[0],
            block_y_size=self.block_shape[1],
            max_records=self.max_records)

    @classmethod
    def regular(cls, name: str, crs: str, cell_size: Union[int, Tuple[int, int]], resolution: float,
                block_size: int = 256, max_records: int = 1000,
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
            max_records=max_records
        )

    @classmethod
    def single_cell(cls, name: str, crs: str, resolution: int,
                    block_size: int = 256, max_records: int = 1000):
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
            max_records=max_records
        )

    @classmethod
    def web_mercator(cls, name: str, z_level: int,
                     block_size: int = 256, max_records: int = 1000):
        """ Define a regular layout using web-mercator projection at a given z_level"""
        ox, oy, semi_axis = -20037508.342789244, 20037508.342789244, 6378137
        resolution = 2*math.pi*semi_axis/(256*(1 << z_level))
        return Layout.regular(name, "epsg:3857", cell_size=(256, 256), resolution=resolution,
                              block_size=block_size, max_records=max_records)

    def __repr__(self):
        return f"Layout '{self.name}'"

    def __str__(self):
        return "Layout '{}'\n" \
               "    grid_flags\n{}\n" \
               "    grid_parameters\n{}\n" \
               "    block_shape  {}\n" \
               "    max_records  {}\n".format(self.name, "      \n".join(self.grid_flags),
                                              pprint.pformat(self.grid_parameters, indent=7, width=1),
                                              self.block_shape, self.max_records)
