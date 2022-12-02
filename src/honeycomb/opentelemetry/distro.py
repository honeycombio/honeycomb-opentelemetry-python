"""
Add module doc string
"""
import os
from opentelemetry.instrumentation.distro import BaseDistro

from opentelemetry.environment_variables import (
    # OTEL_METRICS_EXPORTER,
    OTEL_TRACES_EXPORTER,

)
from opentelemetry.sdk.environment_variables import (
    OTEL_EXPORTER_OTLP_PROTOCOL,
    OTEL_EXPORTER_OTLP_HEADERS,
    OTEL_EXPORTER_OTLP_ENDPOINT
)

HONEYCOMB_API_KEY = "HONEYCOMB_API_KEY"


class HoneycombDistro(BaseDistro):
    """
    The OpenTelemetry provided Distro configures a default set of
    configuration out of the box.
    """
    def _configure(self, **kwargs):
        os.environ.setdefault(OTEL_TRACES_EXPORTER, "otlp")
        os.environ.setdefault(OTEL_EXPORTER_OTLP_PROTOCOL, "grpc")
        # Metrics off by default, will add back in later
        # os.environ.setdefault(OTEL_METRICS_EXPORTER, "otlp"

        apikey = os.environ.get(HONEYCOMB_API_KEY)

        os.environ.setdefault(OTEL_EXPORTER_OTLP_HEADERS, f'x-honeycomb-team={apikey}')

        # this will also be an overrideable default in future
        os.environ.setdefault(OTEL_EXPORTER_OTLP_ENDPOINT, "api.honeycomb.io:443")

        # if there has been an otel service name set, use it
        # otherwise set default OTEL_SERVICE_NAME="unknown_service:python"
