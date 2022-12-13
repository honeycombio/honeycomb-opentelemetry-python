from honeycomb.opentelemetry.options import (
    HONEYCOMB_API_KEY,
    HONEYCOMB_METRICS_APIKEY,
    HONEYCOMB_TRACES_APIKEY,
    OTEL_EXPORTER_METRICS_ENDPOINT,
    OTEL_EXPORTER_TRACES_ENDPOINT,
    HoneycombOptions
)
from opentelemetry.sdk.environment_variables import (
    OTEL_SERVICE_NAME,
    OTEL_EXPORTER_OTLP_ENDPOINT
)

# classic keys are 32 chars long
CLASSIC_APIKEY = "this is a string that is 32 char"
# non-classic keys are 22 chars log
APIKEY = "an api key for 22 char"
CUSTOM_ENDPOINT = "localhost:4317"


def test_defaults(monkeypatch):
    options = HoneycombOptions()
    assert options.apikey == None
    assert options.endpoint == "api.honeycomb.io:443"
    assert options.service_name == "unknown_service:python"


def test_can_set_service_name_with_param(monkeypatch):
    options = HoneycombOptions(service_name='my-service')
    assert options.service_name == 'my-service'


def test_can_set_service_name_with_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_SERVICE_NAME, "my-service")
    options = HoneycombOptions()
    assert options.service_name == 'my-service'


def test_can_set_endpoint_with_param(monkeypatch):
    options = HoneycombOptions(endpoint='localhost:4317')
    assert options.endpoint == 'localhost:4317'


def test_can_set_endpoint_with_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, "localhost:4317")
    options = HoneycombOptions()
    assert options.endpoint == 'localhost:4317'


def test_can_set_traces_endpoint_with_param(monkeypatch):
    options = HoneycombOptions(traces_endpoint=CUSTOM_ENDPOINT)
    assert options.traces_endpoint == CUSTOM_ENDPOINT


def test_can_set_traces_endpoint_with_traces_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_TRACES_ENDPOINT, CUSTOM_ENDPOINT)
    options = HoneycombOptions()
    assert options.traces_endpoint == CUSTOM_ENDPOINT


def test_can_set_traces_endpoint_with_endpoint_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, CUSTOM_ENDPOINT)
    options = HoneycombOptions()
    assert options.traces_endpoint == CUSTOM_ENDPOINT


def test_can_set_metrics_endpoint_with_param(monkeypatch):
    options = HoneycombOptions(metrics_endpoint=CUSTOM_ENDPOINT)
    assert options.metrics_endpoint == CUSTOM_ENDPOINT


def test_can_set_metrics_endpoint_with_metrics_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_METRICS_ENDPOINT, CUSTOM_ENDPOINT)
    options = HoneycombOptions()
    assert options.metrics_endpoint == CUSTOM_ENDPOINT


def test_can_set_metrics_endpoint_with_endpoint_envvar(monkeypatch):
    monkeypatch.setenv(OTEL_EXPORTER_OTLP_ENDPOINT, CUSTOM_ENDPOINT)
    options = HoneycombOptions()
    assert options.metrics_endpoint == CUSTOM_ENDPOINT


def test_get_traces_endpoint_returns_endpoint_when_traces_endpoint_not_set(monkeypatch):
    options = HoneycombOptions(endpoint=CUSTOM_ENDPOINT)
    assert options.get_traces_endpoint() == CUSTOM_ENDPOINT


def test_get_metrics_endpoint_returns_endpoint_when_metricss_endpoint_not_set(monkeypatch):
    options = HoneycombOptions(endpoint=CUSTOM_ENDPOINT)
    assert options.get_metrics_endpoint() == CUSTOM_ENDPOINT


def test_can_set_apikey_with_param(monkeypatch):
    options = HoneycombOptions(apikey=APIKEY)
    assert options.apikey == APIKEY


def test_can_set_apikey_with_envvar(monkeypatch):
    monkeypatch.setenv(HONEYCOMB_API_KEY, APIKEY)
    options = HoneycombOptions()
    assert options.apikey == APIKEY


def test_can_set_traces_apikey_with_param(monkeypatch):
    options = HoneycombOptions(traces_apikey=APIKEY)
    assert options.traces_apikey == APIKEY


def test_can_set_traces_apikey_with_envvar(monkeypatch):
    monkeypatch.setenv(HONEYCOMB_TRACES_APIKEY, APIKEY)
    options = HoneycombOptions()
    assert options.traces_apikey == APIKEY


def test_can_set_metrics_apikey_with_param(monkeypatch):
    options = HoneycombOptions(traces_apikey=APIKEY)
    assert options.traces_apikey == APIKEY


def test_can_set_metrics_apikey_with_envvar(monkeypatch):
    monkeypatch.setenv(HONEYCOMB_METRICS_APIKEY, APIKEY)
    options = HoneycombOptions()
    assert options.metrics_apikey == APIKEY
