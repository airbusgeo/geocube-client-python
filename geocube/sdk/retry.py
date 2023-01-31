import retrying
from geocube import sdk


class ExponentialWait:
    def __init__(self, func_name):
        self.func_name = func_name
        self.exception = None

    def __call__(self, attempts, _):
        delay = 1000*(2**(attempts-1))
        print(f'{self.func_name}: Attempt #{attempts}, retrying in {delay // 1000} seconds' +
              f': {self.exception}' if self.exception is not None else '')
        self.exception = None
        return delay

class CopyException:
    def __init__(self, retry_on_exception, object_with_exception):
        self.retry_on_exception = retry_on_exception
        self.object_with_exception = object_with_exception

    def __call__(self, e):
        retry = self.retry_on_exception(e)
        if retry:
            self.object_with_exception.exception = e
        return retry

def retry_on_geocube_error(func_name: str, max_delay_s: float, error=sdk.is_geocube_error):
    w = ExponentialWait(func_name)
    return retrying.retry(wait_func=w,
                          stop_max_delay=max_delay_s*1000,
                          retry_on_exception=CopyException(error, w))
