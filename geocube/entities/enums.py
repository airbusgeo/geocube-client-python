from enum import Enum

Compression = Enum('Compression', 'NO LOSSLESS LOSSY')

pb_compression = [Compression.NO, Compression.LOSSLESS, Compression.LOSSY]

Resampling = Enum('Resampling', 'undefined near bilinear cubic cubicspline lanczos average mode max min med q1 q3')

pb_resampling = [Resampling.undefined, Resampling.near, Resampling.bilinear, Resampling.cubic, Resampling.cubicspline,
                 Resampling.lanczos, Resampling.average, Resampling.mode, Resampling.max, Resampling.min,
                 Resampling.med, Resampling.q1, Resampling.q3]