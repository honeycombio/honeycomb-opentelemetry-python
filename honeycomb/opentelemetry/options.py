import logging
import os
from opentelemetry.sdk.environment_variables import (
    OTEL_SERVICE_NAME,
    OTEL_EXPORTER_OTLP_ENDPOINT
)
from grpc import ssl_channel_credentials

DEBUG = "DEBUG"
HONEYCOMB_API_KEY = "HONEYCOMB_API_KEY"
HONEYCOMB_TRACES_APIKEY = "HONEYCOMB_TRACES_APIKEY"
HONEYCOMB_METRICS_APIKEY = "HONEYCOMB_METRICS_APIKEY"
OTEL_LOG_LEVEL = "OTEL_LOG_LEVEL"
OTEL_SERVICE_VERSION = "OTEL_SERVICE_VERSION"
OTEL_EXPORTER_TRACES_ENDPOINT = "OTEL_EXPORTER_TRACES_ENDPOINT"
OTEL_EXPORTER_METRICS_ENDPOINT = "OTEL_EXPORTER_METRICS_ENDPOINT"
SAMPLE_RATE = "SAMPLE_RATE"
DEFAULT_API_ENDPOINT = "api.honeycomb.io:443"
DEFAULT_SERVICE_NAME = "unknown_service:python"
DEFAULT_LOG_LEVEL = "ERROR"
DEFAULT_SAMPLE_RATE = 1

log_levels = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

_logger = logging.getLogger(__name__)


class HoneycombOptions:
    apikey = None
    traces_apikey = None
    metrics_apikey = None
    service_name = DEFAULT_SERVICE_NAME
    service_version = None
    endpoint = DEFAULT_API_ENDPOINT
    traces_endpoint = None,
    metrics_endpoint = None,
    insecure = False
    enable_metrics = False
    sample_rate = DEFAULT_SAMPLE_RATE
    debug = False
    log_level = DEFAULT_LOG_LEVEL

    def __init__(
        self,
        apikey: str = None,
        traces_apikey: str = None,
        metrics_apikey: str = None,
        service_name: str = None,
        service_version: str = None,
        endpoint: str = None,
        traces_endpoint: str = None,
        metrics_endpoint: str = None,
        insecure: bool = False,
        sample_rate: int = None,
        debug: bool = False,
        log_level: str = None
    ):
        log_level = os.environ.get(OTEL_LOG_LEVEL, log_level)
        if log_level and log_level.upper() in log_levels:
            self.log_level = log_level.upper()
        logging.basicConfig(level=log_levels[self.log_level])

        self.apikey = os.environ.get(HONEYCOMB_API_KEY, apikey)
        self.traces_apikey = os.environ.get(
            HONEYCOMB_TRACES_APIKEY, traces_apikey)
        self.metrics_apikey = os.environ.get(
            HONEYCOMB_METRICS_APIKEY, metrics_apikey)

        self.service_name = os.environ.get(OTEL_SERVICE_NAME, service_name)
        if not self.service_name:
            # TODO - warn no service name set,
            # defaulting to unknown_service:python
            self.service_name = DEFAULT_SERVICE_NAME
        self.service_version = os.environ.get(
            OTEL_SERVICE_VERSION, service_version)

        self.endpoint = os.environ.get(OTEL_EXPORTER_OTLP_ENDPOINT, endpoint)
        if not self.endpoint:
            self.endpoint = DEFAULT_API_ENDPOINT
        self.traces_endpoint = os.environ.get(
            OTEL_EXPORTER_TRACES_ENDPOINT,
            os.environ.get(
                OTEL_EXPORTER_OTLP_ENDPOINT,
                traces_endpoint
            )
        )
        self.metrics_endpoint = os.environ.get(
            OTEL_EXPORTER_METRICS_ENDPOINT,
            os.environ.get(
                OTEL_EXPORTER_OTLP_ENDPOINT,
                metrics_endpoint
            )
        )

        sample_rate_str = os.environ.get(SAMPLE_RATE, None)
        if sample_rate_str:
            try:
                self.sample_rate = int(sample_rate_str)
            except ValueError:
                _logger.warning(
                    "Unable to parse integer from SAMPLE_RATE enviornment variable. Using sample rate of 1.")
        elif sample_rate:
            self.sample_rate = sample_rate

        debug_str = os.environ.get(DEBUG, None)
        if debug_str:
            try:
                self.debug = bool(debug_str)
            except ValueError:
                _logger.warning(
                    "Unable to parse bool from DEBUG environment variable.")
        else:
            self.debug = debug

        self.insecure = insecure

    def get_traces_apikey(self):
        if self.traces_apikey:
            return self.traces_apikey
        return self.apikey

    def get_metrics_apikey(self):
        if self.metrics_apikey:
            return self.metrics_apikey
        return self.apikey

    def get_traces_endpoint(self):
        if self.traces_endpoint:
            return self.traces_endpoint
        return self.endpoint

    def get_metrics_endpoint(self):
        if self.metrics_endpoint:
            return self.metrics_endpoint
        return self.endpoint

    def get_trace_endpoint_credentials(self):
        # TODO: use trace endpoint
        if self.insecure:
            return None
        return ssl_channel_credentials()

    def get_metrics_endpoint_credentials(self):
        # TODO: use metrics endpoint
        if self.insecure:
            return None
        return ssl_channel_credentials()

    def get_trace_headers(self):
        headers = {
            "x-honeycomb-team": self.get_traces_apikey(),
        }
        return headers

    def get_metrics_headers(self):
        # TODO: use metrics api key & metrics dataset
        headers = {
            "x-honeycomb-team": self.get_metrics_apikey(),
            "x-honeycomb-dataset": self.service_name + "_metrics"
        }
        return headers
