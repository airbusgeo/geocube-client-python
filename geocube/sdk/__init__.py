import os

from geocube.sdk.connection_params import ConnectionParams
from geocube.sdk.collection import Collection
from geocube.sdk.multiprocess import is_pickleable, multiprocess, MessageType, Status, ResultsEncoder, \
    ProcessAbnormalTermination, ProcessTimeoutError, ProcessPicklingError, message_queue_t
from geocube.sdk.catalogue import image_callback_t, image_do_nothing, cube_callback_t, cube_do_nothing,\
    get_cube, get_cubes, is_geocube_error
from geocube.sdk.retry import retry_on_geocube_error

from geocube.sdk.geocube_xarray import GeocubeBackendEntrypoint, open_geocube

assert "GRPC_ENABLE_FORK_SUPPORT" in os.environ and os.environ["GRPC_ENABLE_FORK_SUPPORT"] == "1", \
    "To use this functionality, set the **global** environment variable GRPC_ENABLE_FORK_SUPPORT=1"
