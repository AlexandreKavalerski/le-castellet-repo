import functools
import asyncio
from time import perf_counter
from ..logger import logger
from typing import Callable, Any


def tracktime(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator that tracks the perf_counter time for the executed method and logs it
    """
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_timed(*args: dict | None, **kwargs: dict | None) -> Any:
            ts = perf_counter()
            result = await func(*args, **kwargs)
            te = perf_counter()
            execution_time = (te - ts) * 1000
            module = func.__module__
            method_name = func.__name__

            logger.info(
                f"execution time of method | {module}.{method_name}={execution_time:.2f} ms"
            )
            return result
        return async_timed

    @functools.wraps(func)
    def sync_timed(*args: Any, **kw: Any) -> Any:
        ts = perf_counter()
        result = func(*args, **kw)
        te = perf_counter()
        execution_time = (te - ts) * 1000
        module = func.__module__
        method_name = func.__name__

        logger.info(
            f"execution time of method | {module}.{method_name}={execution_time:.2f} ms"
        )
        return result
    return sync_timed
