import geopandas
import shapely
from shapely import ops


def read_aoi(aoi_file):
    """ Read an AOI from file in geographic coordinates """
    df = geopandas.read_file(aoi_file).to_crs("epsg:4326")
    return shapely.ops.unary_union(list(df.geometry))


def plot_aoi(aoi: geopandas.GeoSeries, world_path: str = geopandas.datasets.get_path('naturalearth_lowres'),
             ax=None, margin_pc=5):
    if world_path is not None:
        base = geopandas.read_file(world_path).plot(color='lightgrey', edgecolor='white', ax=ax)
    else:
        base = ax

    aoi.plot(ax=base, alpha=0.5, edgecolor='gray')
    bounds = aoi.total_bounds
    margin = (margin_pc / 100) * min(bounds[2] - bounds[0], bounds[3] - bounds[1])
    base.set_xlim(bounds[0] - margin, bounds[2] + margin)
    base.set_ylim(bounds[1] - margin, bounds[3] + margin)
    return base
