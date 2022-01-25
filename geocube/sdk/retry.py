import retrying
from geocube import sdk


def _wait(func_name):
    def wait_fn(attempts, _):
        delay = 1000*(2**(attempts-1))
        print(f'{func_name}: Attempt #{attempts}, retrying in {delay // 1000} seconds')
        return delay
    return wait_fn


def retry_on_geocube_error(func_name: str, max_delay_s: float):
    return retrying.retry(wait_func=_wait(func_name),
                          stop_max_delay=max_delay_s*1000,
                          retry_on_exception=sdk.is_geocube_error)
