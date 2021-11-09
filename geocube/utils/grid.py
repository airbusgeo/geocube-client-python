from typing import List

from geocube import entities


def epsg_from_utm(zone: int, row: str) -> int:
    if row == 'A' or row == 'B':
        return 32761
    if row == 'Y' or row == 'Z':
        return 32661
    if row < 'N':
        return 32700+zone
    return 32600+zone


def utm(zones: List[int], rows: List[str], geometries) -> List[entities.Cell]:
    return [entities.Cell.from_geom(f"{zone:02d}{row}", f"epsg:{epsg_from_utm(zone, row)}", geometry)
            for zone, row, geometry in zip(zones, rows, geometries)]
