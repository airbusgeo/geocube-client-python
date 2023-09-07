import warnings

import geopandas
from shapely import ops
try:
    from shapely.errors import GEOSException
except ImportError:
    GEOSException = ValueError

def read_aoi(aoi_file):
    """ Read an AOI from file in geographic coordinates """
    df = geopandas.read_file(aoi_file).to_crs("epsg:4326")
    try:
        return ops.unary_union(list(df.geometry))
    except GEOSException as e:
        warnings.warn(f"{e}. Retrying, trying to make the geometry valid...")
        return ops.unary_union([g.buffer(0) for g in df.geometry])

def gpd_read_remote_file(url):
    import fsspec
    with fsspec.open(f"simplecache::{url}") as file:
        return geopandas.read_file(file)

def plot_aoi(aoi: geopandas.GeoSeries,
             world_path: str = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/"
                               "download/110m/cultural/ne_110m_admin_0_countries.zip",
             ax=None, margin_pc=5):
    if world_path is not None:
        base = gpd_read_remote_file(world_path).plot(color='lightgrey', edgecolor='white', ax=ax)
    else:
        base = ax

    aoi.plot(ax=base, alpha=0.5, edgecolor='gray')
    bounds = aoi.total_bounds
    margin = (margin_pc / 100) * min(bounds[2] - bounds[0], bounds[3] - bounds[1])
    base.set_xlim(bounds[0] - margin, bounds[2] + margin)
    base.set_ylim(bounds[1] - margin, bounds[3] + margin)
    return base
