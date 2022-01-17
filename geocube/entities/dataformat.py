from dataclasses import dataclass, asdict
import numpy as np

from geocube.pb import dataformat_pb2

pb_types = ["undefined", "uint8", "uint16", "uint32", "int8", "int16", "int32", "float32", "float64", "complex64"]


@dataclass(frozen=True)
class DataFormat:
    """
    >>> DataFormat.from_user("u1")
    uint8 [0 255] nodata=0
    >>> DataFormat.from_user(('f4', np.nan, -1, 1))
    float32 [-1.0 1.0] nodata=None
    >>> DataFormat.from_user({'dtype':'u1', 'no_data':0})
    uint8 [0 255] nodata=0
    """
    # TODO prendre en compte les types non numpy ?
    dtype:     str
    min_value: float
    max_value: float
    no_data:   float

    def to_pb(self):
        df = dataformat_pb2.DataFormat(
            dtype=pb_types.index(self.dtype),
            no_data=self.no_data,
            min_value=self.min_value,
            max_value=self.max_value)
        return df

    @classmethod
    def from_pb(cls, pb):
        return cls(
            dtype=pb_types[pb.dtype],
            no_data=pb.no_data,
            min_value=pb.min_value,
            max_value=pb.max_value
        )

    @classmethod
    def from_user(cls, args):
        """
        args=(dtype, no_data, min_value, max_value))
        args=dtype
        args={'dtype':..., 'no_date':..., 'min_value':..., 'max_value':...}
        """
        if isinstance(args, DataFormat):
            return cls.from_dict(asdict(args))
        if isinstance(args, str):
            args = args.split(",")
        if isinstance(args, (tuple, list)):
            d = {'dtype': args[0]}
            if len(args) > 1:
                d['no_data'] = float(args[1])
            if len(args) > 2:
                d['min_value'] = float(args[2])
            if len(args) > 3:
                d['max_value'] = float(args[3])
        else:
            d = args

        if isinstance(d, dict):
            return cls.from_dict(d)

        cls.__raise_format_error(d)

    @classmethod
    def from_dict(cls, d: dict):
        try:
            dtype = d['dtype']
            if dtype == "" or dtype == pb_types[0] or dtype == "auto":
                return cls(pb_types[0],
                           d.get('min_value', 0),
                           d.get('max_value', -1),
                           d.get('no_data', float('nan')))

            dtype = np.dtype(dtype)
            if dtype.kind in 'iu':
                info = np.iinfo(dtype)
                nan_, min_, max_ = info.min, info.min, info.max
            elif dtype.kind in 'fc':
                info = np.finfo(dtype)
                nan_, min_, max_ = np.nan, info.min, info.max
            else:
                nan_, min_, max_ = 0, 0, 1

            no_data = d.get('no_data', nan_)
            if not np.isnan(no_data):
                no_data = dtype.type(no_data)

            return cls(dtype.name,
                       dtype.type(d.get('min_value', min_)),
                       dtype.type(d.get('max_value', max_)),
                       no_data)
        except KeyError:
            cls.__raise_format_error(d)

    @classmethod
    def __raise_format_error(cls, e):
        raise ValueError("DataFormat : Unsupported format ({})".format(e))

    def __repr__(self):
        return "{} [{} {}] nodata={}".format(self.dtype, self.min_value, self.max_value, self.no_data)
