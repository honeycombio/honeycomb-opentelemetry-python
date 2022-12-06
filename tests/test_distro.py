import os

from opentelemetry.environment_variables import OTEL_TRACES_EXPORTER
from opentelemetry.sdk.environment_variables import (
    OTEL_SERVICE_NAME,
    OTEL_EXPORTER_OTLP_PROTOCOL,
    OTEL_EXPORTER_OTLP_HEADERS,
    OTEL_EXPORTER_OTLP_ENDPOINT
)
from opentelemetry.metrics import get_meter_provider
from opentelemetry.trace import get_tracer_provider

from honeycomb.opentelemetry.options import (
    HONEYCOMB_API_KEY
)
from honeycomb.opentelemetry.distro import (
    configure_opentelemetry
)

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

    exporter = tracer_provider._active_span_processor._span_processors[0].span_exporter
    print(vars(exporter._client.Export._channel))
    assert exporter._client.endpoint == "api.honeycomb.io:443"
    assert exporter.insecure == False
    assert exporter._headers == {}

    # assert os.environ.get(OTEL_SERVICE_NAME) == "unknown_service:python"
    # assert os.environ.get(OTEL_TRACES_EXPORTER) == "otlp"
    # assert os.environ.get(OTEL_EXPORTER_OTLP_PROTOCOL) == "grpc"
    # assert os.environ.get(
    #     OTEL_EXPORTER_OTLP_ENDPOINT) == "api.honeycomb.io:443"
    # assert os.environ.get(OTEL_EXPORTER_OTLP_HEADERS) is None


# def test_can_set_service_name_with_param(monkeypatch):
#     monkeypatch.delenv(OTEL_SERVICE_NAME, raising=False)
#     configure_opentelemetry(service_name='my-service')
#     assert os.environ.get(OTEL_SERVICE_NAME) == 'my-service'


# def test_can_set_service_name_with_envvar(monkeypatch):
#     monkeypatch.setenv(OTEL_SERVICE_NAME, "my-service")
#     configure_opentelemetry()
#     assert os.getenv(OTEL_SERVICE_NAME) == 'my-service'


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
