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
from typing import Dict, Callable, Optional, Any

import pebble
import sys
import traceback
import time
from datetime import datetime, timedelta
from enum import Enum
import queue


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


class Message:
    def __init__(self, _id, _type: MessageType, value, args=None):
        self.id = _id
        self.type = _type
        self.value = value
        self.args = args
        self.date = datetime.today()


class Process:
    def __init__(self, _id: str, func: Callable[[Optional[mp.Queue]], Any], max_attempts):
        self.id = _id
        self.func = func
        self.status = Status.NEW
        self.future = None
        self.result = None
        self.start_time = None
        self.elapsed_time = None
        self.attempts = 0
        self.max_attempts = max_attempts
        self.progress = 0
        self.progress_update = None

    def start(self, pool: mp.Pool, start_func, task_done_func, timeout_sec):
        if self.max_attempts is None or self.attempts < self.max_attempts:
            self.update_status(Status.NEW)
            self.future = pool.schedule(start_func, [self.id, self.func], timeout=timeout_sec)
            self.future.add_done_callback(functools.partial(task_done_func, _id=self.id))
            self.attempts += 1
        else:
            raise ValueError(f'[{self.id}]: Max attempts reached')

    def update_status(self, new_status: Status, args=None):
        if new_status == Status.NEW:
            if self.status == Status.DONE:
                raise ValueError(f'[{self.id}]: Cannot start a process already done')
            self.status = Status.NEW
            self.progress = 0
            self.result = None

        if new_status == Status.PENDING:
            if self.status == Status.DONE or self.status == Status.FAILED:
                raise ValueError(f'[{self.id}]: Cannot mark pending a process done or failed')
            self.status = Status.PENDING
            self.start_time = args

        elif new_status == Status.DONE:
            if self.status == Status.FAILED:
                raise ValueError(f'[{self.id}]: Cannot finish a failed process')
            if self.status == Status.DONE:
                raise ValueError(f'[{self.id}]: Cannot finish a process already done')
            self.status = Status.DONE
            self.elapsed_time = datetime.today() - self.start_time
            self.future = None
            self.result = args

        elif new_status == Status.FAILED:
            if self.status == Status.DONE:
                raise ValueError(f'[{self.id}]: Cannot fail a process done')
            if self.status == Status.FAILED:
                raise ValueError(f'[{self.id}]: Cannot fail a process already failed')
            self.status = Status.FAILED
            self.elapsed_time = datetime.today() - self.start_time if self.start_time is not None else 0
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
                self.update_status(Status.FAILED, args)

    def update_progress(self, progress):
        self.progress = progress
        self.progress_update = datetime.today()

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


def count_active(processes: Dict[str, Process]) -> int:
    return len([0 for p in processes.values() if p.status not in (Status.FAILED, Status.DONE)])


def multiprocess(funcs: Dict[str, Callable[[Optional[mp.Queue]], Any]], children: int = None,
                 max_tasks_per_child: int = 0, timeout_sec: int = None, retry_on_error: Callable[[Any], bool] = None,
                 max_attempts: int = None, log_prefix: str = None, log_lvl=logging.INFO, checkpoint_dir: str = None):
    if len(funcs) == 0:
        return {}

    # Check funcs are pickleable
    for f in funcs.values():
        assert is_pickleable(f), f"{f} is not pickleable"

    if checkpoint_dir:
        os.makedirs(checkpoint_dir, exist_ok=True)
    logger.setLevel(log_lvl)

    # Prepare the data
    children = mp.cpu_count() if children is None else children
    processes = {_id: Process(_id, func, max_attempts) for _id, func in funcs.items()}
    manager = mp.Manager()
    state_queue = manager.Queue()
    log_queue = manager.Queue()

    start_func = functools.partial(_async_func, mq=state_queue, log_queue=log_queue, log_prefix=log_prefix)
    task_done_func = functools.partial(_task_done, mq=state_queue, retry_on_error=retry_on_error)

    sleep_sec = 1  # timeout_sec/10 if timeout_sec and timeout_sec < 10 else 1

    with pebble.ProcessPool(max_workers=children, max_tasks=max_tasks_per_child) as pool:
        for process in processes.values():
            process.start(pool, start_func, task_done_func, timeout_sec)

        c_full_status = c_status = -1
        print_status = False
        checkpoint = False
        while count_active(processes) > 0:
            # Scan state_queue
            for message in _QueueIterator(state_queue, False):
                if message.type == MessageType.STATUS:
                    try:
                        processes[message.id].update_status(message.value, message.args)
                        logger.info(f'{message.date}: [{message.id}] new status : {message.value} '
                                    f'[{_truncate_fmt(message.args, 100)}]')
                    except ValueError as e:
                        logger.error(e)
                    checkpoint = True
                    print_status = True

            # Scan log_queue
            for message in _QueueIterator(log_queue, False):
                if message.type == MessageType.PROGRESS:
                    processes[message.id].update_progress(message.value)
                    logger.debug(f'{message.date}: [{message.id}] {100*message.value:.0f}%')

            # Scan timeout
            if timeout_sec is not None:
                for process in processes.values():
                    if process.status == Status.PENDING and\
                            process.start_time + timedelta(seconds=timeout_sec+100*sleep_sec) < datetime.today():
                        print_status = True
                        logger.error(f"[{process.id}] Timeout error !! Process looks stuck ({process.start_time})")
                        try:
                            process.update_status(Status.FAILED, ProcessTimeoutError("Unrecoverable timeout"))
                        except ValueError as e:
                            logger.error(e)

            # Retry
            for process in processes.values():
                if process.status == Status.RETRY:
                    process.start(pool, start_func, task_done_func, timeout_sec)
                    logger.info(f"[{process.id}] will restart later")
                    print_status = True

            # Sleep and print status on demand
            time.sleep(sleep_sec)
            c_full_status = c_full_status + 1
            if c_full_status % 1800 == 0:  # Full report every 30 minutes
                _print_full_status(processes)

            if print_status:
                print_status = False
                if c_status < 0:
                    c_status = max((100+c_status, 1))

            c_status -= 1
            if c_status == 0:
                _print_status(processes)

            if checkpoint and checkpoint_dir:
                checkpoint = False
                try:
                    with open(os.path.join(checkpoint_dir, f"checkpoint-{datetime.today()}.json"), "w") as f:
                        json.dump({p.id: (p.status.name, p.result) for p in processes.values()}, f, cls=ResultsEncoder)
                except Exception as e:
                    logger.error(e)

    state_queue.join()
    log_queue.join()
    manager.shutdown()

    # At the end, print full status
    _print_full_status(processes)

    # Return results
    return {p.id: (p.status.name, p.result) for p in processes.values()}


def _format_pending_state(process):
    txt = f'  [{process.id}] pending since {process.start_time:%Y-%m-%d %H:%M} [Attempt: {process.attempts}]'
    if process.progress_update:
        txt += f' {process.progress * 100:.0f}% (last update: {process.progress_update:%Y-%m-%d %H:%M})'
    return txt


def _print_full_status(processes):
    if logger.level > logging.INFO:
        return
    logger.info(f"************** Full Status {datetime.today()} ***************")
    for process in processes.values():
        if process.status == Status.NEW:
            logger.info(f'  [{process.id}] new')
        elif process.status == Status.PENDING:
            logger.info(_format_pending_state(process))
        elif process.status == Status.DONE:
            logger.info(f'  [{process.id}] done in {process.elapsed_time} ({_truncate_fmt(process.result, 30)})')
        elif process.status == Status.FAILED:
            logger.info(f'  [{process.id}] failed in {process.elapsed_time} ({_truncate_fmt(process.result[0], 30)}')
    logger.info("********************************************************************")


def _print_status(processes):
    if logger.level < logging.INFO:
        return
    logger.info(f"************** Status {datetime.today()} ***************")
    count = {Status.NEW: 0, Status.PENDING: 0, Status.DONE: 0, Status.FAILED: 0, Status.RETRY: 0}
    for process in processes.values():
        if process.status == Status.PENDING:
            logger.info(_format_pending_state(process))
        count[process.status] += 1
    for k, c in count.items():
        logger.info(f'  {k.name}: {c}')
    logger.info("********************************************************************")


def _task_done(future, _id: str, mq: mp.Queue, retry_on_error=None):
    try:
        result = future.result(0)
        logger.debug(f'[{_id}]: TaskDone ({_truncate_fmt(result, 100)})')
        Process.message(mq, _id, MessageType.STATUS, Status.DONE, result)

    except pebble.common.ProcessExpired as error:
        logger.debug(f'[{_id}]: ProcessExpired')
        Process.message(mq, _id, MessageType.STATUS, Status.RETRY, (ProcessAbnormalTermination(error),
                                                                    traceback.format_exc()))
    except futures.TimeoutError as error:
        logger.debug(f'[{_id}]: Timeout')
        Process.message(mq, _id, MessageType.STATUS, Status.RETRY, (ProcessTimeoutError(error), traceback.format_exc()))

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

    Process.message(mq, _id, MessageType.STATUS, Status.PENDING, datetime.today())
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
    except (pickle.UnpicklingError, pickle.PickleError, AttributeError, EOFError, ImportError, IndexError, Exception):
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


class _QueueIterator:
    def __init__(self, q: mp.Queue, block=True, timeout=None):
        self.queue = q
        self.block = block
        self.timeout = timeout

    def __iter__(self):
        return self

    def __next__(self):
        try:
            item = self.queue.get(self.block, self.timeout)
            self.queue.task_done()
            return item
        except queue.Empty:
            raise StopIteration
