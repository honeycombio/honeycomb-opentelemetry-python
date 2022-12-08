import platform

import pytest
from honeycomb.opentelemetry.distro import configure_opentelemetry
from honeycomb.opentelemetry.options import HONEYCOMB_API_KEY
from honeycomb.opentelemetry.version import __version__
from opentelemetry.environment_variables import OTEL_TRACES_EXPORTER
from opentelemetry.sdk.environment_variables import (
    OTEL_SERVICE_NAME,
    OTEL_EXPORTER_OTLP_PROTOCOL,
    OTEL_EXPORTER_OTLP_HEADERS,
    OTEL_EXPORTER_OTLP_ENDPOINT
)
from opentelemetry.metrics import get_meter_provider
from opentelemetry.trace import get_tracer_provider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.distro import BaseDistro

from pkg_resources import DistributionNotFound, require


# classic keys are 32 chars long
CLASSIC_APIKEY = "this is a string that is 32 char"
# non-classic keys are 22 chars log
APIKEY = "an api key for 22 char"


def test_distro_configure_defaults(monkeypatch):
    monkeypatch.delenv(OTEL_SERVICE_NAME, raising=False)
    monkeypatch.delenv(OTEL_TRACES_EXPORTER, raising=False)
    monkeypatch.delenv(OTEL_EXPORTER_OTLP_PROTOCOL, raising=False)
    monkeypatch.delenv(OTEL_EXPORTER_OTLP_ENDPOINT, raising=False)
    monkeypatch.delenv(OTEL_EXPORTER_OTLP_HEADERS, raising=False)

    configure_opentelemetry()
    tracer_provider = get_tracer_provider()
    assert tracer_provider._resource._attributes["service.name"] == "unknown_service:python"
    assert tracer_provider._resource._attributes["honeycomb.distro.version"] == __version__
    assert tracer_provider._resource._attributes["honeycomb.distro.runtime_version"] == platform.python_version(
    )
    # spanExporter = tracer_provider._active_span_processor._span_processors[0].span_exporter
    # assert isinstance(spanExporter, OTLPSpanExporter)

    meter_provider = get_meter_provider()
    assert len(meter_provider._meters) == 0


def test_can_set_service_name_with_param(monkeypatch):
    monkeypatch.delenv(OTEL_SERVICE_NAME, raising=False)
    configure_opentelemetry(service_name="my-service")
    tracer_provider = get_tracer_provider()
    print(vars(tracer_provider._resource._attributes))
    assert tracer_provider._resource._attributes["service.name"] == "my-service"


# def test_can_set_endpoint_with_param(monkeypatch):
#     monkeypatch.delenv(OTEL_EXPORTER_OTLP_ENDPOINT, raising=False)
#     configure_opentelemetry(endpoint='localhost:4317')
#     assert os.environ.get(OTEL_EXPORTER_OTLP_ENDPOINT) == 'localhost:4317'


# def test_can_set_endpoint_with_envvar(monkeypatch):
#     monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, "localhost:4317")
#     configure_opentelemetry()
#     assert os.environ.get(OTEL_EXPORTER_OTLP_ENDPOINT) == 'localhost:4317'


# def test_can_set_apikey_with_param(monkeypatch):
#     monkeypatch.delenv(HONEYCOMB_API_KEY, raising=False)
#     configure_opentelemetry(apikey=APIKEY)
#     assert os.environ.get(
#         OTEL_EXPORTER_OTLP_HEADERS) == f'x-honeycomb-team={APIKEY}'


# def test_can_set_apikey_with_envvar(monkeypatch):
#     monkeypatch.setenv(HONEYCOMB_API_KEY, APIKEY)
#     configure_opentelemetry()
#     assert os.environ.get(
#         OTEL_EXPORTER_OTLP_HEADERS) == f'x-honeycomb-team={APIKEY}'


def test_package_available():
    try:
        require(["opentelemetry-distro"])
    except DistributionNotFound:
        pytest.fail("opentelemetry-distro not installed")
