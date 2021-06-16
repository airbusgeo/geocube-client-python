import calendar

from google.protobuf import wrappers_pb2 as wrappers, timestamp_pb2


def pb_string(value: str):
    return None if value is None else wrappers.StringValue(value=value)


def pb_null_timestamp() -> timestamp_pb2.Timestamp:
    """ Returns a null pb2_timestamp (timestamp_pb2.Timestamp() is not Null)"""
    return timestamp_pb2.Timestamp(seconds=calendar.timegm((1, 1, 0, 0, 0, 0)))
