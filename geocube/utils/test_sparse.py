import numpy as np

from geocube.utils.sparse_full_array import SparseFullArray


class TestSparse:
    def test_sparse(self):
        shape = (6, 6, 3)
        for i in range(len(shape)):
            print("sparse_axis=", i)
            a = SparseFullArray(shape, sparse_axis=i)
            assert np.all(np.isnan(np.asarray(a)))

            a = SparseFullArray(shape, sparse_axis=i)
            a[0] = np.zeros((6, 3))
            assert np.all(np.isnan(np.asarray(a)[1:]))
            assert np.all(np.asarray(a)[0] == 0)



