import os
from opentelemetry.sdk.environment_variables import (
    OTEL_SERVICE_NAME,
    OTEL_EXPORTER_OTLP_ENDPOINT
)


HONEYCOMB_API_KEY = "HONEYCOMB_API_KEY"
HONEYCOMB_API_ENDPOINT = "HONEYCOMB_API_ENDPOINT"
DEFAULT_API_ENDPOINT = "api.honeycomb.io:443"
DEFAULT_SERVICE_NAME = "unknown_service:python"


class HoneycombOptions:
    apikey = None
    service_name = DEFAULT_SERVICE_NAME
    endpoint = DEFAULT_API_ENDPOINT
    insecure = False
    enable_metrics = False

    def __init__(self, apikey: str = None, service_name: str = None, endpoint: str = None, insecure: bool = False, enable_metrics: bool = False):
        self.apikey = os.environ.get(HONEYCOMB_API_KEY, apikey)

        self.service_name = os.environ.get(OTEL_SERVICE_NAME, service_name)
        if not self.service_name:
            # TODO - warn no service name set, defaulting to unknown_service:python
            self.service_name = DEFAULT_SERVICE_NAME

        self.endpoint = os.environ.get(OTEL_EXPORTER_OTLP_ENDPOINT, endpoint)
        if not self.endpoint:
            self.endpoint = DEFAULT_API_ENDPOINT

        self.insecure = insecure
        self.enable_metrics = enable_metrics
