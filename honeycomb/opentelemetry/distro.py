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
    service_name: str = DEFAULT_SERVICE_NAME,
    endpoint: str = DEFAULT_API_ENDPOINT
):
    print(os.environ.setdefault(OTEL_SERVICE_NAME, os.environ.get(
        OTEL_SERVICE_NAME, service_name)))
    os.environ.setdefault(OTEL_SERVICE_NAME, os.environ.get(
        OTEL_SERVICE_NAME, service_name))

    os.environ.setdefault(OTEL_TRACES_EXPORTER, "otlp")
    # disable metrics for now
    os.environ.setdefault(OTEL_METRICS_EXPORTER, "none")
    os.environ.setdefault(OTEL_EXPORTER_OTLP_PROTOCOL, "grpc")

    os.environ.setdefault(
        OTEL_EXPORTER_OTLP_ENDPOINT, endpoint)

    if apikey:
        os.environ.setdefault(OTEL_EXPORTER_OTLP_HEADERS,
                              f"x-honeycomb-team={apikey}")


class HoneycombDistro(BaseDistro):
    """
    The OpenTelemetry provided Distro configures a default set of
    configuration out of the box.
    """

    def _configure(self, **kwargs):
        configure_opentelemetry()
