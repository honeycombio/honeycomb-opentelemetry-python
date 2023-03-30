from opentelemetry.sdk.metrics import MeterProvider

from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.metrics import create_meter_provider


def test_returns_meter_provider():
    options = HoneycombOptions()
    resource = create_resource(options)
    meter_provider = create_meter_provider(options, resource)
    assert isinstance(meter_provider, MeterProvider)
    assert len(meter_provider._sdk_config.metric_readers) == 1


def test_setting_debug_adds_console_exporter():
    options = HoneycombOptions(debug=True)
    resource = create_resource(options)
    meter_provider = create_meter_provider(options, resource)
    assert isinstance(meter_provider, MeterProvider)
    assert len(meter_provider._sdk_config.metric_readers) == 2
