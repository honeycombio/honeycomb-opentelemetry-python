from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.trace import create_tracer_provider
from opentelemetry.sdk.trace import TracerProvider


def test_returns_tracer_provider():
    options = HoneycombOptions()
    resource = create_resource(options)
    provider = create_tracer_provider(options, resource)
    assert isinstance(provider, TracerProvider)
