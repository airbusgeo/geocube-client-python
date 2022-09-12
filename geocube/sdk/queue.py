import multiprocessing as mp
import pickle
import queue
from typing import Union

from dask import distributed


class DaskQueue(distributed.Queue):
    def put(self, o: object, **kwargs):
        return super(DaskQueue, self).put(pickle.dumps(o), **kwargs)

    def get(self, **kwargs):
        if self.qsize() == 0:
            raise queue.Empty
        return pickle.loads(super(DaskQueue, self).get(**kwargs))

    def __len__(self):
        return self.qsize()

    def join(self):
        super(DaskQueue, self).get(batch=True)
        self.close()

    def task_done(self):
        pass


class _QueueIterator:
    def __init__(self, q: Union[DaskQueue, mp.Queue], timeout=None):
        self.queue = q
        self.timeout = timeout
        self.kwargs = {} if isinstance(self.queue, DaskQueue) else {"block": False}

    def __iter__(self):
        return self

    def __len__(self):
        return self.queue.qsize()

    def __next__(self):
        try:
            item = self.queue.get(timeout=self.timeout, **self.kwargs)
            self.queue.task_done()
            return item
        except queue.Empty:
            raise StopIteration
