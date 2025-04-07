import functools
import warnings

def deprecated(message):
    def deprecated_decorator(func):
        @functools.wraps(func)
        def deprecated_func(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(f"{func.__name__} is a deprecated function. {message}",
                          category=DeprecationWarning,
                          stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)
        return deprecated_func
    return deprecated_decorator