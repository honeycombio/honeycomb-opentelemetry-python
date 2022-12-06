from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.metrics import create_meter_provider
from opentelemetry.sdk.metrics import MeterProvider


def test_returns_meter_provider():
    options = HoneycombOptions()
    resource = create_resource(options)
    provider = create_meter_provider(options, resource)
    assert isinstance(provider, MeterProvider)
