from typing import Tuple, List

import numpy as np
from xarray.core import indexing as xarray_indexing

from geocube.utils import indexing


class SparseFullArray:
    def __init__(self, shape: tuple, sparse_axis: int):
        if sparse_axis < 0:
            sparse_axis = len(shape)+sparse_axis
        assert 0 <= sparse_axis < len(shape)
        self.shape = shape
        self.axis = sparse_axis
        self.data = {}

    def __setitem__(self, key, value):
        key = xarray_indexing.expanded_indexer(key, len(self.shape))
        k = key[self.axis]
        if isinstance(k, int):
            k = slice(k, k+1, None)
        for i in range(*k.indices(self.shape[self.axis])):
            self.data[i] = value[self._idx(key, i)]

    def __getitem__(self, key):
        sparse_key, other_keys = self._sparse_key(key)
        if sparse_key == slice(None, None, None):
            if other_keys == indexing.empty(len(self.shape)-1):
                return self
            return np.asarray(self)[key]
        start, stop, step, _ = indexing.key_to_range(sparse_key, self.shape[self.axis])
        if start == stop-1:
            return self.data[start][other_keys]
        new_sparse = SparseFullArray(self._idx(self.shape, (stop-start)//step), self.axis)
        new_sparse.data = {j: self.data[i] for j, i in enumerate(range(start, stop, step)) if i in self.data}
        return np.asarray(new_sparse)[key]

    def put(self, key, value):
        self.data[key] = value

    def collapse(self) -> Tuple[np.ndarray, List[int]]:
        idx = sorted(self.data)
        return np.stack([self.data[k] for k in idx]), idx

    def __array__(self):
        if len(self.data) == self.shape[self.axis]:
            return np.stack([self.data[k] for k in sorted(self.data)], axis=self.axis)

        ret = np.empty(self.shape)
        idx = indexing.empty(len(self.shape))
        for i in range(self.shape[self.axis]):
            ret[self._idx(idx, i)] = self.data[i] if i in self.data else np.nan
        return ret

    def _idx(self, idx: tuple, val):
        return idx[:self.axis] + (val,) + idx[self.axis+1:]

    def _sparse_key(self, key):
        key = xarray_indexing.expanded_indexer(key, len(self.shape))
        return key[self.axis], key[:self.axis] + key[self.axis+1:]
