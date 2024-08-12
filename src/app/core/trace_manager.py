import functools
import asyncio
from time import perf_counter
from contextlib import contextmanager
import sentry_sdk
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.opentelemetry import SentrySpanProcessor, SentryPropagator
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from typing import Callable, Any

from ..core.logger import logger
from ..core.config import settings
from ..core.db.database import async_engine


class TraceManager():
    def __init__(self) -> None:
        logger.info('initializing tracer with configs')
        env = settings.ENVIRONMENT
        if (env not in ['test', 'staging', 'homologation']):
            logger.info('Sentry enabled')
            sentry_sdk.init(
                dsn=settings.SENTRY_HOST,
                traces_sample_rate=settings.SENTRY_SAMPLING_RATE,
                # debug=settings.SENTRY_ENABLE_DEBUG,
                enable_tracing=settings.SENTRY_IS_ENABLED,
                instrumenter='otel',
                environment=settings.SENTRY_ENV_LABEL,
                integrations=[
                    SqlalchemyIntegration(),
                    FastApiIntegration(
                        transaction_style="endpoint",
                        failed_request_status_codes=[403, range(500, 599)],
                    ),
                ]
            )

        self.enabled = False
        tracing_enable = settings.SENTRY_IS_ENABLED

        self.service_name = settings.SENTRY_SERVICE_NAME
        self.resource = Resource(attributes={
            SERVICE_NAME: self.service_name
        })

        provider = TracerProvider(resource=self.resource)
        provider.add_span_processor(SentrySpanProcessor())
        trace.set_tracer_provider(provider)
        set_global_textmap(SentryPropagator())

        B3MultiFormat._SAMPLE_PROPAGATE_VALUES = {"1", "True", "true", "d", "0"}
        set_global_textmap(B3MultiFormat())
        self.fastapi_instrumentor = FastAPIInstrumentor()
        self.sqlalchemy_instrumentor = SQLAlchemyInstrumentor()
        self.start_fastapi = False

        if tracing_enable and env != 'test':
            self.enable()
        else:
            self.disable()

    def get_tracer(self):
        return trace.get_tracer(__name__)

    def start_fastapi_instrumentation(self) -> None:
        if self.enabled and not self.start_fastapi:
            self.fastapi_instrumentor.instrument()
            self.start_fastapi = True

    def enable_sqlalchemy_instrumentation(self) -> None:
        self.sqlalchemy_instrumentor.instrument(engine=async_engine.sync_engine)

    def disable_sqlalchemy_instrumentation(self) -> None:
        self.sqlalchemy_instrumentor.uninstrument()

    def enable(self) -> None:
        self.enabled = True
        self.enable_sqlalchemy_instrumentation()
        self.start_fastapi_instrumentation()

    def disable(self) -> None:
        if self.enabled:
            self.disable_sqlalchemy_instrumentation()
            self.fastapi_instrumentor.uninstrument()
            self.start_fastapi = False
        self.enabled = False


trace_manager_inst = TraceManager()

@contextmanager
def timing_and_trace_context(description: str, **kwargs: dict | None) -> None:
    ts = perf_counter()
    if trace_manager_inst.enabled:
        tracer = trace_manager_inst.get_tracer()
        with tracer.start_as_current_span(name="{}".format(description)):
            yield
    else:
        yield

    te = perf_counter()
    elapsed_time = (te - ts) * 1000

    logger.debug(f"execution time of block | {description}={elapsed_time:.2f} ms")


def trace_and_timeit(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to instrument a function and log its execution time."""
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args: dict | None, **kwargs: dict | None) -> Any:
            method_name = func.__qualname__
            with timing_and_trace_context(description=method_name):
                return await func(*args, **kwargs)
        return async_wrapper

    @functools.wraps(func)
    def sync_wrapper(*args: dict | None, **kwargs: dict | None) -> Any:
        method_name = func.__qualname__
        with timing_and_trace_context(description=method_name):
            return func(*args, **kwargs)
    return sync_wrapper
