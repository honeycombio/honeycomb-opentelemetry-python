import os

from opentelemetry.environment_variables import OTEL_TRACES_EXPORTER
from opentelemetry.sdk.environment_variables import (
    OTEL_EXPORTER_OTLP_PROTOCOL,
    OTEL_EXPORTER_OTLP_HEADERS,
    OTEL_EXPORTER_OTLP_ENDPOINT
)

from honeycomb.opentelemetry.distro import (
    HoneycombDistro,
    HONEYCOMB_API_KEY
)

# classic keys are 32 chars long
CLASSIC_APIKEY = "this is a string that is 32 char"
# non-classic keys are 22 chars log
APIKEY = "an api key for 22 char"


def test_distro_configure_defaults():
    my_distro = HoneycombDistro()
    assert os.environ.get(OTEL_TRACES_EXPORTER) is None
    assert os.environ.get(OTEL_EXPORTER_OTLP_PROTOCOL) is None
    assert os.environ.get(OTEL_EXPORTER_OTLP_HEADERS) is None
    os.environ.setdefault(HONEYCOMB_API_KEY, APIKEY)
    
    my_distro.configure()
    assert os.environ.get(OTEL_TRACES_EXPORTER) == "otlp"
    assert os.environ.get(OTEL_EXPORTER_OTLP_PROTOCOL) == "grpc"
    assert os.environ.get(OTEL_EXPORTER_OTLP_HEADERS) == f'x-honeycomb-team={APIKEY}'
    assert os.environ.get(OTEL_EXPORTER_OTLP_ENDPOINT) == "api.honeycomb.io:443"

# def test_distro_configure_overrides
    # service name
    # endpoint, too
