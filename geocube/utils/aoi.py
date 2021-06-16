import geopandas
import shapely
from shapely import ops


def read_aoi(aoi_file):
    """ Read an AOI from file in geographic coordinates """
    df = geopandas.read_file(aoi_file).to_crs("epsg:4326")
    return shapely.ops.unary_union(list(df.geometry))
