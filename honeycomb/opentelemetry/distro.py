"""
Add module doc string
"""
import os
from opentelemetry.instrumentation.distro import BaseDistro
from opentelemetry.environment_variables import OTEL_TRACES_EXPORTER, OTEL_METRICS_EXPORTER
from opentelemetry.sdk.environment_variables import (
    OTEL_SERVICE_NAME,
    OTEL_EXPORTER_OTLP_PROTOCOL,
    OTEL_EXPORTER_OTLP_HEADERS,
    OTEL_EXPORTER_OTLP_ENDPOINT
)

HONEYCOMB_API_KEY = "HONEYCOMB_API_KEY"
HONEYCOMB_API_ENDPOINT = "HONEYCOMB_API_ENDPOINT"

DEFAULT_API_ENDPOINT = "api.honeycomb.io:443"
DEFAULT_SERVICE_NAME = "unknown_service:python"


def configure_opentelemetry(
    apikey: str = None,
    service_name: str = None,
    endpoint: str = None
):
    os.environ.setdefault(OTEL_EXPORTER_OTLP_PROTOCOL, "grpc")
    os.environ.setdefault(OTEL_TRACES_EXPORTER, "otlp")
    # disable metrics for now
    os.environ.setdefault(OTEL_METRICS_EXPORTER, "none")

    service_name = os.environ.get(OTEL_SERVICE_NAME, service_name)
    if not service_name:
        # TODO - warn no service name set, defaulting to unknown_service:python
        service_name = DEFAULT_SERVICE_NAME
    os.environ.setdefault(OTEL_SERVICE_NAME, service_name)

    endpoint = os.environ.get(OTEL_EXPORTER_OTLP_ENDPOINT, endpoint)
    if not endpoint:
        endpoint = DEFAULT_API_ENDPOINT
    os.environ.setdefault(OTEL_EXPORTER_OTLP_ENDPOINT, endpoint)

    apikey = os.environ.get(HONEYCOMB_API_KEY, apikey)
    if apikey:
        os.environ.setdefault(OTEL_EXPORTER_OTLP_HEADERS,
                              f"x-honeycomb-team={apikey}")
    else:
        # TODO - warn no API key set
        pass


class HoneycombDistro(BaseDistro):
    """
    The OpenTelemetry provided Distro configures a default set of
    configuration out of the box.
    """

    def _configure(self, **kwargs):
        configure_opentelemetry()
