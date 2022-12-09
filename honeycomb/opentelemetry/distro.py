"""
Add module doc string
"""
from honeycomb.opentelemetry.metrics import create_meter_provider
from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.trace import create_span_exporter
from opentelemetry.instrumentation.distro import BaseDistro
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter
)
from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.metrics import MeterProvider


def configure_opentelemetry(
    apikey: str = None,
    service_name: str = None,
    endpoint: str = None
):
    options = HoneycombOptions(
        apikey=apikey,
        service_name=service_name,
        endpoint=endpoint
    )

    resource = create_resource(options)

    # force tracer & meter providers to be set :sadpanda:
    # if os.getenv("OTEL_PYTHON_TRACER_PROVIDER", None) is None:
    # if isinstance(get_tracer_provider(), ProxyTracerProvider):
    set_tracer_provider(TracerProvider(resource=resource))
    # set_meter_provider(MeterProvider())

    # create exporter and add to exiting tracer provider
    exporter = create_span_exporter(options)
    trace_provider = get_tracer_provider()
    trace_provider._resource = resource
    trace_provider.add_span_processor(
        BatchSpanProcessor(exporter)
    )
    trace_provider.add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )

    if options.enable_metrics:
        set_meter_provider(
            create_meter_provider(options, resource)
        )


class HoneycombDistro(BaseDistro):
    """
    This honey-flavored Distro configures OpenTelemetry for use with Honeycomb.
    """

    def _configure(self, **kwargs):
        print('🐝 auto instrumented 🐝')
        configure_opentelemetry()
