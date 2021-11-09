from typing import Union, List
import geopandas as gpd

from geocube import entities


EntityIdable = Union[str, entities.Record, entities.VariableInstance, entities.Layout, entities.Job, gpd.GeoDataFrame]


def get_ids(ents: Union[EntityIdable, List[EntityIdable]]) -> List[str]:
    """ Returns a list of ids given something that have an id """
    if isinstance(ents, gpd.GeoDataFrame):
        return list(ents['id'])
    try:
        return [get_id(ents)]
    except TypeError:
        return [get_id(entity) for entity in ents]


def get_id(entity: EntityIdable) -> str:
    """ Returns an id given something that have an id """
    if isinstance(entity, str):
        return entity
    if isinstance(entity, entities.Record) or isinstance(entity, entities.Job):
        return entity.id
    if isinstance(entity, entities.Layout):
        return entity.name
    if isinstance(entity, entities.VariableInstance):
        return entity.instance_id
    if isinstance(entity, gpd.GeoDataFrame) and len(entity.index) == 1:
        return entity["id"].iloc[0]
    raise TypeError
