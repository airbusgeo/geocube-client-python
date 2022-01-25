import functools
import logging
import sys
import time
from random import random

from geocube.sdk import MessageType, multiprocess, Status, ProcessAbnormalTermination, ProcessTimeoutError, \
    ProcessPicklingError


def rand_sleep_success(max_time):
    time.sleep(random()*max_time)
    return True


def rand_sleep_failed(max_time):
    time.sleep(random()*max_time)
    raise NameError("Rand Error")


global_retries = 0
global_kill = 0
nb_retries = 0


def n_errors():
    global nb_retries
    if nb_retries > 0:
        nb_retries -= 1
        raise ValueError("Rand Error")
    return True


def retry_on_value_error(error):
    global global_retries
    global_retries += 1
    return isinstance(error, ValueError)


def rand_timeout(delay, probability):
    if random() < probability:
        time.sleep(delay)
    return True


def func_log_queue(mp_log_queue=None):
    if mp_log_queue is not None:
        mp_log_queue(MessageType.PROGRESS, 0.5)
    return True


class UnpicklableError(Exception):
    def __init__(self, too, many, arguments, to, be, picklable):
        self.too = too
        self.remain = (many, arguments, to, be, picklable)
        super().__init__("unpicklable")


def unpicklable_error():
    raise UnpicklableError("too", "many", "arguments", "to", "be", "picklable")


def unpicklable_return():
    return UnpicklableError("too", "many", "arguments", "to", "be", "picklable")


class TestMultiProcess:
    def test_success(self):
        t = 2
        funcs = {str(i): functools.partial(rand_sleep_success, t) for i in range(10)}
        results = multiprocess(funcs, children=None, timeout_sec=t, log_lvl=logging.DEBUG)

        for i, r in results.items():
            assert r[0] == Status.DONE
            assert r[1] is True

    def test_failed(self):
        t = 2
        funcs = {str(i): functools.partial(rand_sleep_failed, t) for i in range(10)}
        results = multiprocess(funcs, children=None, timeout_sec=t, log_lvl=logging.DEBUG)

        for i, r in results.items():
            assert r[0] == Status.FAILED
            assert isinstance(r[1][0], NameError)

    def test_retry(self):
        global global_retries, nb_retries
        global_retries = 0
        nb_retries = 3
        children = 4
        funcs = {str(i): n_errors for i in range(10)}
        results = multiprocess(funcs, children=children, timeout_sec=1, log_lvl=logging.DEBUG,
                               retry_on_error=retry_on_value_error)

        for i, r in results.items():
            assert r[0] == Status.DONE
            assert r[1] is True
        assert global_retries == nb_retries*children

    def test_kill(self):
        global global_retries
        global_retries = 0
        t = 2
        funcs = {str(i): sys.exit for i in range(10)}
        results = multiprocess(funcs, children=None, timeout_sec=t, log_lvl=logging.DEBUG,
                               retry_on_error=retry_on_value_error, max_attempts=3)

        for i, r in results.items():
            assert r[0] == Status.FAILED
            assert isinstance(r[1][0], ProcessAbnormalTermination)

    def test_success_with_timeout(self):
        global global_retries
        global_retries = 0
        t = 2
        funcs = {str(i): functools.partial(rand_timeout, t, 0.7) for i in range(10)}
        results = multiprocess(funcs, children=None, timeout_sec=t//2, log_lvl=logging.DEBUG,
                               retry_on_error=retry_on_value_error, max_attempts=None)

        for i, r in results.items():
            assert r[0] == Status.DONE
            assert r[1] is True
        assert global_retries == 0

    def test_failed_with_timeout(self):
        global global_retries
        global_retries = 0
        t = 2
        funcs = {str(i): functools.partial(time.sleep, t) for i in range(10)}
        results = multiprocess(funcs, children=None, timeout_sec=t//2, log_lvl=logging.DEBUG,
                               retry_on_error=retry_on_value_error, max_attempts=2)
        for i, r in results.items():
            assert r[0] == Status.FAILED
            assert isinstance(r[1][0], ProcessTimeoutError)
        assert global_retries == 0

    def test_log_queue(self):
        t = 2
        funcs = {str(i): func_log_queue for i in range(10)}
        results = multiprocess(funcs, children=None, timeout_sec=t//2, log_lvl=logging.DEBUG,
                               retry_on_error=None, max_attempts=None)
        for i, r in results.items():
            assert r[0] == Status.DONE
            assert r[1] is True

    def test_unpicklable_error(self):
        t = 2
        funcs = {str(i): unpicklable_error for i in range(10)}
        results = multiprocess(funcs, children=None, timeout_sec=t//2, log_lvl=logging.DEBUG,
                               retry_on_error=None, max_attempts=2)
        for i, r in results.items():
            assert r[0] == Status.FAILED
            assert isinstance(r[1][0], ProcessPicklingError)

    def test_unpicklable_return(self):
        t = 2
        funcs = {str(i): unpicklable_return for i in range(10)}
        results = multiprocess(funcs, children=None, timeout_sec=t//2, log_lvl=logging.DEBUG,
                               retry_on_error=None, max_attempts=2)
        for i, r in results.items():
            assert r[0] == Status.FAILED
            assert isinstance(r[1][0], ProcessPicklingError)
