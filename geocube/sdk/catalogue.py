import functools
import time
from typing import Union, List, Callable, Any, Dict, Tuple, Optional

import affine
import numpy as np
from geocube.entities import cubeiterator

import geocube
from geocube import entities, sdk
from geocube.sdk import ConnectionParams
from geocube.sdk.multiprocess import _has_parameter
from geocube.utils import GeocubeError


image_callback_t = Union[
    Callable[[np.ndarray,                        # `image`
              Optional[List[entities.Record]],   # `grouped_records`
              Optional[str],                     # `crs` or `projection`
              Optional[affine.Affine],           # `transform`
              ],
             np.ndarray],
    functools.partial
]
"""
image_callback_t is the prototype of a function called for every image received by a sdk.get_cube().
It can be used to process each new image on the fly during a get_cube process.
If they are parameter of the function, the standard parameters `image`, `grouped_records`, `crs` or `projection` and
`transform` will be automatically provided by get_cube().
The function has to return an image.
eg.:
    def process_image(image):
        return image.astype(float)/255
    
eg.:
    def process_image(image, grouped_records, crs, transform):
        utils.image_to_geotiff(image, crs, transform, 0, f"{grouped_records[0].datetime}.tiff")
        return image
"""

cube_callback_t = Union[
    Callable[[np.ndarray,                              # `timeseries` or `cube`
              Optional[List[List[entities.Record]]],   # `grouped_records`
              Optional[str],                           # `crs` or `projection`
              Optional[affine.Affine],                 # `transform`
              Optional[entities.VariableInstance]      # `variable` or `instance` (only with get_cubes, not get_cube)
              ], Any],
    functools.partial
]
"""
cube_callback_t is the prototype of a function called with the results of a get_cube (timeseries, records).
If they are parameter of the function, the standard parameters `timeseries` or 'cube', `grouped_records`, `variable`, 
`instance`, `crs` or `projection` and `transform`  will be automatically provided by get_cube()
The function can return whatever user wants.
eg.:
    def process_timeseries(timeseries, grouped_records, crs, transform, variable):
        mean = np.nanmean(timeseries, axis=0)
        utils.image_to_geotiff(mean, crs, transform, variable.dformat.no_data, f"{grouped_records[0].datetime}.tiff")
        return "success"
"""


def cube_do_nothing(cube: np.ndarray, grouped_records: List[List[entities.Record]], **_):
    """ cube_callback_t, return the cube and the grouped_records """
    return cube, grouped_records


def image_do_nothing(image: np.ndarray, **_):
    """ image_callback_t, doing nothing, returning input image """
    return image


def is_geocube_error(error):
    return isinstance(error, GeocubeError)


def get_cube(connection_params: ConnectionParams, cube_params: entities.CubeParams,
             image_callback: image_callback_t = image_do_nothing, cube_callback: cube_callback_t = cube_do_nothing,
             compression: int = 0, verbose: bool = False, mp_log_queue: sdk.message_queue_t = None)\
        -> Tuple[np.array, List[entities.GroupedRecords]]:
    """
    A wrapper on client.get_cube, adding a call to 'image_callback' on each slice of the cube (cf client.get_cube)
    and an optional call to 'cube_callback' on the cube.
    Args:
        connection_params: to connect to the Geocube
        cube_params: see geocube.Client.get_cube
        image_callback: a function called for each slice of the cube (by default: do_nothing)
        cube_callback: a function called for each cube (by default: do_nothing)
        mp_log_queue: a callable to receive logs and progress updates
        verbose: see geocube.Client.get_cube
        compression: see geocube.Client.get_cube
    """
    geo_params = {
        "crs": cube_params.crs,
        "projection": cube_params.crs,
        "transform": cube_params.transform
    }

    image_cb = _partial_func(image_callback, **geo_params)
    images, records = _get_cube(connection_params.new_client(with_downloader=True),
                                cube_params, image_cb, compression, verbose, mp_log_queue)

    if cube_callback is not None:
        return _partial_func(cube_callback,
                             cube=images,
                             timeseries=images,
                             grouped_records=records,
                             **geo_params)()
    return images, records


def get_cubes(connection_params: ConnectionParams, cube_params: entities.CubeParams, variables: Dict[str, str],
              image_callback: image_callback_t = image_do_nothing, cube_callback: cube_callback_t = cube_do_nothing,
              compression: int = 0, verbose: bool = False, mp_log_queue: sdk.message_queue_t = None):
    """
    A loop over a call to client.get_cube for each variable, adding a call to 'image_callback' on each slice of the cube
    and a call to 'cube_callback' on each cube
    Args:
        connection_params: to connect to the Geocube
        cube_params: see geocube.Client.get_cube
        variables: list of variables (couples of (variable, instance)) to be retrieved
        image_callback: a function called for each slice of the cube (by default: do_nothing)
        cube_callback: a function called for each cube (by default: do_nothing)
        verbose: see geocube.Client.get_cube
        compression: see geocube.Client.get_cube
        mp_log_queue: a callable to receive logs and progress updates
    """
    client = connection_params.new_client(with_downloader=True)

    geo_params = {
        "crs": cube_params.crs,
        "projection": cube_params.crs,
        "transform": cube_params.transform
    }

    results = {}
    for i, (variable, instance) in enumerate(variables.items()):
        # Load instance
        vi = client.variable(variable).instance(instance)
        cube_params.instance = vi

        # Define callback function
        image_cb = _partial_func(image_callback, instance=vi, variable=vi, **geo_params)

        # Get cube and apply image_callback on each image
        cube, grouped_records = _get_cube(client, cube_params, image_cb, compression, verbose)

        # Apply cube_callback on the result
        results[f"{variable}.{instance}"] = _partial_func(cube_callback,
                                                          cube=cube,
                                                          timeseries=cube,
                                                          grouped_records=grouped_records,
                                                          variable=vi,
                                                          instance=vi,
                                                          **geo_params)()

        # log progress
        if mp_log_queue:
            mp_log_queue(sdk.MessageType.PROGRESS, (i + 1) / len(variables))

    return results


def _get_cube(client: geocube.Client, cube_params: entities.CubeParams,
              callback: image_callback_t, compression: int = 0,
              verbose: bool = False, mp_log_queue: sdk.message_queue_t = None)\
        -> Tuple[np.array, List[entities.GroupedRecords]]:
    def log(text):
        if mp_log_queue is not None:
            mp_log_queue(sdk.MessageType.LOG, text)
        else:
            print(text)

    start_time = time.time()

    # Get cube_iterator
    cube = client.get_cube_it(cube_params, compression=compression)

    if verbose:
        log(f"Receiving {cube.count} images")
    total_size = 0

    grouped_records_list = []
    timeseries = np.empty((0,))

    try:
        for image, metadata, err in cube:
            if err is not None:
                if err == cubeiterator.NOT_FOUND_ERROR:
                    continue
                raise ValueError(err)
            total_size += metadata.bytes//1024
            if len(timeseries) == 0:
                timeseries = np.empty((cube.count, *image.shape))
            if callback is not None:
                timeseries[cube.index] = _partial_func(callback,
                                                       image=image,
                                                       grouped_records=metadata.grouped_records)()
            else:
                timeseries[cube.index] = image
            grouped_records_list.append(metadata.grouped_records)

        # log progress
        if mp_log_queue is not None:
            mp_log_queue(sdk.MessageType.PROGRESS, ((cube.index+1) / max(cube.count, 1)))

        if verbose:
            log(f"Received and processed {len(cube)} images in {time.time()-start_time}s ({total_size//1024}Mb ~"
                f"{(total_size/len(cube)) if len(cube) >0 else 0}kb.im)")

        return np.resize(timeseries, (len(cube), *timeseries.shape[1:])), grouped_records_list

    except GeocubeError:
        log(f'Fail to receive all the images ({time.time()-start_time}s)')
        raise


def _partial_func(callback_func, **optional_parameters):
    if callback_func is None:
        return None
    for param_name in list(optional_parameters.keys()):
        if not _has_parameter(callback_func, param_name):
            del optional_parameters[param_name]
    if len(optional_parameters) > 0:
        return functools.partial(callback_func, **optional_parameters)
    return callback_func
