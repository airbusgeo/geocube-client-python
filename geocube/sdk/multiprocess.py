import enum
import functools
import inspect
import json
import logging
import multiprocessing as mp
import os
import pickle
from concurrent import futures
from json import JSONEncoder
from typing import Dict, Callable, Optional, Any, Union

import dask
import pebble
import distributed
import sys
import traceback
import time
from datetime import datetime, timedelta
from enum import Enum
import queue

from tqdm import tqdm

from geocube.sdk.queue import _QueueIterator, DaskQueue
import pytz


class MessageType(Enum):
    STATUS = enum.auto()
    PROGRESS = enum.auto()
    LOG = enum.auto()


class Status(Enum):
    NEW = enum.auto()
    PENDING = enum.auto()
    DONE = enum.auto()
    RETRY = enum.auto()
    FAILED = enum.auto()


logger = logging.getLogger("geocube_multiprocess")

""" message_queue_t can be used for logging or for progress updating in an asynchronous function """
message_queue_t = Optional[Callable[[MessageType, Any], None]]


class ResultsEncoder(JSONEncoder):
    """ To JSON-encode results (especially errors) """
    def default(self, o):
        return o.__repr__()


class ProcessTimeoutError(Exception):
    """The operation exceeded the given deadline."""
    pass


class ProcessAbnormalTermination(pebble.ProcessExpired):
    """The process terminated unexpectedly."""
    pass


class ProcessPicklingError(pickle.PicklingError):
    """The process returned or raised something un-pickleable."""
    pass


def date_diff(date1, date2):
    tz1, tz2 = date1.tzinfo, date2.tzinfo
    if tz1 != tz2:
        print("date1 and date2 have different timezone...")
        if tz1:
            return date1-date2.astimezone(tz1)
        return date1.astimezone(tz2)-date2
    return date1-date2


def now():
    return datetime.now(pytz.utc)


def elapsed(date):
    return date_diff(now(), date)


class Message:
    def __init__(self, _id, _type: MessageType, value, args=None):
        self.id = _id
        self.type = _type
        self.value = value
        self.args = args
        self.date = now()


class LogProgress:
    def __init__(self, iterable, log_queue, log_every_pc=10):
        self.iterable = iterable
        self.log_queue = log_queue
        self.count = 0
        self.length = len(iterable)
        self.log_every = (self.length*log_every_pc)//100

    def __iter__(self):
        self.count = 0
        self.iterator = iter(self.iterable)
        return self

    def __next__(self):
        if self.log_queue is not None and self.log_every:
            if (self.count-1)//self.log_every != self.count//self.log_every:
                self.log_queue(MessageType.PROGRESS, self.count/self.length)
            self.count += 1
        return next(self.iterator)


class LogQueueHandler(logging.Handler):
    def __init__(self, log_putter: Callable[[MessageType, str], Any]):
        super().__init__()
        self.log_putter = log_putter

    def emit(self, record: logging.LogRecord) -> None:
        self.log_putter(MessageType.LOG, record.getMessage())


class Process:
    def __init__(self, _id: str, func: Callable[[Optional[mp.Queue]], Any], max_attempts, start_func, task_done_func):
        self.id = _id
        self.func = func
        self.start_func = start_func
        self.task_done_func = functools.partial(task_done_func, _id=self.id)
        self.status = Status.NEW
        self.future = None
        self.result = None
        self.start_time = None
        self.elapsed_time = None
        self.attempts = 0
        self.max_attempts = max_attempts
        self.progress = 0
        self.progress_update = None

    def start(self, client: Union[pebble.ProcessPool, distributed.Client], timeout_sec):
        if self.max_attempts is None or self.attempts < self.max_attempts:
            self.update_status(Status.NEW, now())
            if isinstance(client, pebble.ProcessPool):
                self.future = client.schedule(self.start_func, [self.id, self.func], timeout=timeout_sec)
            elif isinstance(client, distributed.Client):
                self.future = client.compute(dask.delayed(self.start_func)(self.id, self.func))
            self.future.add_done_callback(self.task_done_func)
            self.attempts += 1
        else:
            raise ValueError(f'[{self.id}]: Max attempts reached')

    def update_status(self, new_status: Status, date, args=None):
        logger.info(f'{date:%Y-%m-%d %H:%M}: [{self.id}] new status : {new_status} [{_truncate_fmt(args, 100)}]')
        if new_status == Status.NEW:
            if self.status == Status.DONE:
                raise ValueError(f'[{self.id}]: Cannot start a process already done')
            self.status = Status.NEW
            self.progress = 0
            self.result = None

        elif new_status == Status.PENDING:
            if self.status == Status.DONE or self.status == Status.FAILED:
                raise ValueError(f'[{self.id}]: Cannot mark pending a process done or failed')
            self.status = Status.PENDING
            self.start_time = date

        elif new_status == Status.DONE:
            if self.status == Status.FAILED:
                raise ValueError(f'[{self.id}]: Cannot finish a failed process')
            if self.status == Status.DONE:
                raise ValueError(f'[{self.id}]: Cannot finish a process already done')
            self.status = Status.DONE
            self.elapsed_time = date_diff(date, self.start_time)
            self.future = None
            self.result = args

        elif new_status == Status.FAILED:
            if self.status == Status.DONE:
                raise ValueError(f'[{self.id}]: Cannot fail a process done')
            if self.status == Status.FAILED:
                raise ValueError(f'[{self.id}]: Cannot fail a process already failed')
            self.status = Status.FAILED
            self.elapsed_time = date_diff(date, self.start_time) if self.start_time is not None else 0
            self.future = None
            if args is not None:
                self.result = args

        elif new_status == Status.RETRY:
            if self.status == Status.DONE or self.status == Status.FAILED:
                raise ValueError(f'[{self.id}]: Cannot retry a process done or failed')
            if self.status == Status.RETRY:
                raise ValueError(f'[{self.id}]: Cannot retry a process already retried')
            if self.max_attempts is None or self.attempts < self.max_attempts:
                self.status = Status.RETRY
            else:
                self.update_status(Status.FAILED, date, args)

    def update_progress(self, progress):
        self.progress = progress
        self.progress_update = now()

    @staticmethod
    def message(q: mp.Queue, _id: str, _type: MessageType, value, args):
        try:
            logger.debug(f'[{_id}]: Post message {_type}: {_truncate_fmt(value, 100)}')
            q.put(Message(_id, _type, value, args), timeout=60)

        except queue.Full as e:
            logger.error(f"Full queue ({e}) : unable to post {_type.name}:{value} [{args}]")
        except ConnectionRefusedError as e:
            logger.error(f"Connection refused ({e}) : unable to post {_type.name}:{value} [{args}]")
        except Exception as e:
            raise Exception(f"Unable to post message {_type.name}:{value} [{args}]: {e}")


class MultiProcesses:
    """
    Handle multiprocess tasks with DaskClient or PeeblePool
    >>> with pebble.ProcessPool(max_workers=1, max_tasks=1) as client:
    ...      mprocesses = MultiProcesses(client, [print])
    ...      results = mprocesses.join()
    >>> print(results)
    >>> with distributed.Client() as client:
    ...      mprocesses = MultiProcesses(client, [print])
    ...      results = mprocesses.join()
    """
    def __init__(self,
                 client: Union[pebble.ProcessPool, distributed.Client],
                 funcs: Dict[str, Callable[[Optional[mp.Queue]], Any]],
                 own_client: bool = False,
                 timeout_sec: int = None, retry_on_error: Callable[[Any], bool] = None,
                 max_attempts: int = None, log_prefix: str = None, log_lvl=logging.INFO, checkpoint_dir: str = None,
                 check_pickling: bool = True):

        if len(funcs) == 0:
            self.processes = None
            return

        # Check funcs are pickleable
        if check_pickling:
            for f in funcs.values():
                assert is_pickleable(f), f"{f} is not pickleable"

        # Configuration
        self.timeout_sec = timeout_sec
        self.checkpoint_dir = checkpoint_dir
        if checkpoint_dir:
            os.makedirs(checkpoint_dir, exist_ok=True)
        logger.setLevel(log_lvl)
        logger.addHandler(logging.StreamHandler(stream=sys.stderr))

        # Client
        self.client = client
        self.close_client = own_client

        # Create Queues
        if isinstance(client, distributed.Client):
            self.state_queue, self.log_queue, self.manager = DaskQueue(client=client), DaskQueue(client=client), None
        else:
            self.manager = mp.Manager()
            self.state_queue, self.log_queue = self.manager.Queue(), self.manager.Queue()

        # Prepare the data
        start_func = functools.partial(_async_func, mq=self.state_queue,
                                       log_queue=self.log_queue, log_prefix=log_prefix)
        task_done_func = functools.partial(_task_done, mq=self.state_queue, retry_on_error=retry_on_error)
        self.processes = {_id: Process(_id, func, max_attempts, start_func, task_done_func)
                          for _id, func in funcs.items()}

        # Start
        for process in self.processes.values():
            process.start(client, timeout_sec)

    def count_active(self) -> int:
        return len([0 for p in self.processes.values() if p.status not in (Status.FAILED, Status.DONE)])

    def update(self):
        sleep_sec = 1  # timeout_sec/10 if timeout_sec and timeout_sec < 10 else 1
        checkpoint, print_status = False, False
        # Scan state_queue
        for message in _QueueIterator(self.state_queue):
            if message.type == MessageType.STATUS:
                try:
                    self.processes[message.id].update_status(message.value, message.date, message.args)
                except ValueError as e:
                    logger.error(e)
                checkpoint = True
                print_status = True

        # Scan log_queue
        q = _QueueIterator(self.log_queue)
        for message in (tqdm(q) if self.log_queue.qsize() > 10 else q):
            if message.type == MessageType.PROGRESS:
                self.processes[message.id].update_progress(message.value)
                logger.debug(f'{message.date}: [{message.id}] {100 * message.value:.0f}%')
            elif message.type == MessageType.LOG:
                logger.info(f'{message.date}: [{message.id}] {message.value}')

        # Scan timeout
        if self.timeout_sec is not None:
            for process in self.processes.values():
                if process.status == Status.PENDING and \
                        elapsed(process.start_time) > timedelta(seconds=self.timeout_sec + 100 * sleep_sec):
                    print_status = True
                    logger.error(f"[{process.id}] Timeout error !! Process looks stuck ({process.start_time})")
                    try:
                        process.update_status(Status.FAILED, now(), ProcessTimeoutError("Unrecoverable timeout"))
                    except ValueError as e:
                        logger.error(e)

        # Retry
        for process in self.processes.values():
            if process.status == Status.RETRY:
                process.start(self.client, self.timeout_sec)
                logger.info(f"[{process.id}] will restart later")
                print_status = True

        if checkpoint:
            self.save_checkpoint()

        return print_status

    def save_checkpoint(self):
        if self.checkpoint_dir:
            try:
                with open(os.path.join(self.checkpoint_dir, f"checkpoint-{datetime.now()}.json"), "w") as f:
                    json.dump({p.id: (p.status.name, p.result) for p in self.processes.values()}, f, cls=ResultsEncoder)
            except Exception as e:
                logger.error(e)

    def join(self):
        sleep_sec = 1  # timeout_sec/10 if timeout_sec and timeout_sec < 10 else 1
        c_full_status = c_status = -1
        old_progress = 0
        try:
            while self.count_active() > 0:
                print_status = self.update()

                # Sleep and print status on demand
                time.sleep(sleep_sec)
                c_full_status = c_full_status + 1
                if c_full_status % 1800 == 0:  # Full report every 30 minutes
                    self.print_full_status()

                if print_status and c_status < 0:
                    c_status = max((100+c_status, 1))

                c_status -= 1
                if c_status == 0:
                    self.print_status()

                progress = int(self.get_progress()*100)
                if progress > old_progress:
                    old_progress = progress
                    logger.info(f"Progress {progress}%")
        except Exception as e:
            print(e)
        finally:
            self.close()

        # At the end, print full status
        self.print_full_status()
        return self.results()

    def close(self):
        try:
            self.state_queue.join()
            self.log_queue.join()
            if self.manager is not None:
                self.manager.shutdown()
        finally:
            if self.close_client:
                self.client.close()

    def results(self):
        return {p.id: (p.status.name, p.result) for p in self.processes.values()}

    def print_full_status(self):
        if logger.level > logging.INFO:
            return
        logger.info(f"************** Full Status {datetime.now()} {100*self.get_progress():.0f}% ***************")
        for process in self.processes.values():
            if process.status == Status.NEW:
                logger.info(f'  [{process.id}] new')
            elif process.status == Status.PENDING:
                logger.info(_format_pending_state(process))
            elif process.status == Status.DONE:
                logger.info(f'  [{process.id}] done in {process.elapsed_time} ({_truncate_fmt(process.result, 30)})')
            elif process.status == Status.FAILED:
                logger.info(f'  [{process.id}] failed in {process.elapsed_time} '
                            f'({_truncate_fmt(process.result[0], 30)}')
        logger.info("********************************************************************")

    def print_status(self):
        if logger.level < logging.INFO:
            return
        logger.info(f"************** Status {datetime.now()} {100*self.get_progress():.0f}% ***************")
        count = {Status.NEW: 0, Status.PENDING: 0, Status.DONE: 0, Status.FAILED: 0, Status.RETRY: 0}
        for process in self.processes.values():
            if process.status == Status.PENDING:
                logger.info(_format_pending_state(process))
            count[process.status] += 1
        for k, c in count.items():
            logger.info(f'  {k.name}: {c}')
        logger.info("********************************************************************")

    def get_progress(self):
        progress = 0
        for process in self.processes.values():
            if process.status == Status.DONE or process.status == Status.FAILED:
                progress += 1
            elif process.status == Status.PENDING:
                progress += process.progress
        return progress/len(self.processes)


def _format_pending_state(process):
    txt = f'  [{process.id}] pending since {process.start_time:%Y-%m-%d %H:%M} [Attempt: {process.attempts}]'
    if process.progress_update:
        txt += f' {process.progress * 100:.0f}% (last update: {process.progress_update:%Y-%m-%d %H:%M})'
    return txt


def _task_done(future, _id: str, mq: mp.Queue, retry_on_error=None):
    try:
        result = future.result()
        logger.debug(f'[{_id}]: TaskDone ({_truncate_fmt(result, 100)})')
        Process.message(mq, _id, MessageType.STATUS, Status.DONE, result)

    except pebble.common.ProcessExpired as error:
        logger.debug(f'[{_id}]: ProcessExpired')
        Process.message(mq, _id, MessageType.STATUS, Status.RETRY, (ProcessAbnormalTermination(error),
                                                                    traceback.format_exc()))
    except futures.TimeoutError as error:
        logger.debug(f'[{_id}]: Timeout')
        Process.message(mq, _id, MessageType.STATUS, Status.RETRY, (ProcessTimeoutError(error), traceback.format_exc()))

    except distributed.scheduler.KilledWorker as error:
        logger.debug(f'[{_id}]: KilledWorker')
        Process.message(mq, _id, MessageType.STATUS, Status.RETRY, (ProcessAbnormalTermination(error),
                                                                    traceback.format_exc()))

    except Exception as error:
        if retry_on_error and retry_on_error(error):
            logger.debug(f'[{_id}]: Function raised "{error}"... retrying')
            status = Status.RETRY
        else:
            logger.debug(f'[{_id}]: Function raised "{error}"\n{traceback.format_exc()}')
            status = Status.FAILED
        Process.message(mq, _id, MessageType.STATUS, status, (error, traceback.format_exc()))


def _async_func(_id, func, mq: mp.Queue, log_queue: mp.Queue = None, log_prefix=None):
    if log_prefix is not None:
        sys.stdout = open(f'{log_prefix}_{_id}.txt', "a+", 1)
        sys.stderr = open(f'{log_prefix}_{_id}_Err.txt', "a+", 1)

    Process.message(mq, _id, MessageType.STATUS, Status.PENDING, None)
    try:
        if log_queue is not None and _has_parameter(func, "mp_log_queue"):
            result = func(mp_log_queue=_log_queue_func(log_queue, _id))
        else:
            result = func()

        logger.debug(f'[{_id}]: Function returned "{_truncate_fmt(result, 100)}"')

        if is_pickleable(result):
            return result
        raise ProcessPicklingError(f'"{result}" is not pickleable')

    except Exception as error:
        if is_pickleable(error):
            raise
        logger.debug(f'[{_id}]: Unpickleable Exception raised {error}')
        raise ProcessPicklingError(f"{error} is not pickleable")


def is_pickleable(obj):
    try:
        pickle.loads(pickle.dumps(obj))
        return True
    except (pickle.UnpicklingError, pickle.PickleError, AttributeError, EOFError, ImportError, IndexError, Exception)\
            as e:
        logger.error(str(e))
        return False


def _has_parameter(func, parameter):
    try:
        return parameter in inspect.signature(func).parameters
    except (ValueError, TypeError):
        return False


def _log_queue_func(log_queue: mp.Queue, _id: str):
    def _log_queue_put(_type: MessageType, value):
        log_queue.put(Message(_id, _type, value, None))
    return _log_queue_put


def _truncate_fmt(value, length) -> str:
    s = f"{value}".replace('\n', '')
    return f"%.*s..." % (length, s) if len(s) > length else s


def _traceback(error, depth) -> str:
    def frame(tb, d, i):
        if d == 0 or tb is None:
            return [None]
        return [f"{i}: {tb.tb_frame}"] + frame(tb.tb_next, d-1, i+1)
    return "\n".join(filter(None, frame(error.__traceback__, depth, 0)))


