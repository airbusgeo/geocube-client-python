from enum import Enum


class Compression(Enum):
    NO = 1
    LOSSLESS = 2
    LOSSY = 3
    CUSTOM = 4


pb_compression = [Compression.NO, Compression.LOSSLESS, Compression.LOSSY, Compression.CUSTOM]


class Resampling(Enum):
    undefined = 1
    near = 2
    bilinear = 3
    cubic = 4
    cubicspline = 5
    lanczos = 6
    average = 7
    mode = 8
    max = 9
    min = 10
    med = 11
    q1 = 12
    q3 = 13


pb_resampling = [Resampling.undefined, Resampling.near, Resampling.bilinear, Resampling.cubic, Resampling.cubicspline,
                 Resampling.lanczos, Resampling.average, Resampling.mode, Resampling.max, Resampling.min,
                 Resampling.med, Resampling.q1, Resampling.q3]
