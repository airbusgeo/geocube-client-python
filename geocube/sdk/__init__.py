import os

from geocube.sdk.aoi import tile_aoi
from geocube.sdk.connection_params import ConnectionParams
from geocube.sdk.collection import Collection
from geocube.sdk.multiprocess import is_pickleable, MultiProcesses, MessageType, Status, ResultsEncoder, \
    ProcessAbnormalTermination, ProcessTimeoutError, ProcessPicklingError, message_queue_t
from geocube.sdk.catalogue import image_callback_t, image_do_nothing, cube_callback_t, cube_do_nothing, \
    get_cube, get_cubes
from geocube.utils.retry import retry_on_geocube_error, is_geocube_error  # For retro compatibility

assert "GRPC_ENABLE_FORK_SUPPORT" in os.environ and os.environ["GRPC_ENABLE_FORK_SUPPORT"] == "1", \
    "To use this functionality, set the **global** environment variable GRPC_ENABLE_FORK_SUPPORT=1"
