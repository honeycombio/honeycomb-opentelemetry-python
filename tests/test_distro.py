import platform

from honeycomb.opentelemetry.distro import configure_opentelemetry
from honeycomb.opentelemetry.version import __version__
from opentelemetry.metrics import get_meter_provider
from opentelemetry.trace import get_tracer_provider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


# classic keys are 32 chars long
CLASSIC_APIKEY = "this is a string that is 32 char"
# non-classic keys are 22 chars log
APIKEY = "an api key for 22 char"


def test_distro_configure_defaults():
    configure_opentelemetry()
    tracer_provider = get_tracer_provider()
    assert tracer_provider._resource._attributes["service.name"] == "unknown_service:python"
    assert tracer_provider._resource._attributes["honeycomb.distro.version"] == __version__
    assert tracer_provider._resource._attributes["honeycomb.distro.runtime_version"] == platform.python_version(
    )
    spanExporter = tracer_provider._active_span_processor._span_processors[0].span_exporter
    assert isinstance(spanExporter, OTLPSpanExporter)

    meter_provider = get_meter_provider()
    assert len(meter_provider._meters) == 0
