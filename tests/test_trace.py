from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.trace import create_span_exporter
from opentelemetry.sdk.trace import TracerProvider


def test_returns_tracer_provider():
    options = HoneycombOptions()
    exporter = create_span_exporter(options)
    # assert isinstance(exporter, TracerProvider)
