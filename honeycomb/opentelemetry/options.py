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
HONEYCOMB_DATASET = "HONEYCOMB_DATASET"
HONEYCOMB_METRICS_DATASET = "HONEYCOMB_METRICS_DATASET"
OTEL_LOG_LEVEL = "OTEL_LOG_LEVEL"
OTEL_SERVICE_VERSION = "OTEL_SERVICE_VERSION"
OTEL_EXPORTER_TRACES_ENDPOINT = "OTEL_EXPORTER_TRACES_ENDPOINT"
OTEL_EXPORTER_METRICS_ENDPOINT = "OTEL_EXPORTER_METRICS_ENDPOINT"
OTEL_EXPORTER_OTLP_INSECURE = "OTEL_EXPORTER_OTLP_INSECURE"
OTEL_EXPORTER_OTLP_TRACES_INSECURE = "OTEL_EXPORTER_OTLP_TRACES_INSECURE"
OTEL_EXPORTER_OTLP_METRICS_INSECURE = "OTEL_EXPORTER_OTLP_METRICS_INSECURE"
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


def is_clasic(apikey: str):
    return apikey and len(apikey) == 32

class HoneycombOptions:
    traces_apikey = None
    metrics_apikey = None
    service_name = DEFAULT_SERVICE_NAME
    service_version = None
    traces_endpoint = None,
    metrics_endpoint = None,
    traces_endpoint_insecure = False,
    metrics_endpoint_insecure = False,
    sample_rate = DEFAULT_SAMPLE_RATE
    debug = False
    log_level = DEFAULT_LOG_LEVEL
    dataset = None
    metrics_dataset = None

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
        endpoint_insecure: bool = False,
        traces_endpoint_insecure: bool = False,
        metrics_endpoint_insecure: bool = False,
        sample_rate: int = None,
        debug: bool = False,
        log_level: str = None,
        dataset: str = None,
        metrics_dataset: str = None
    ):
        log_level = os.environ.get(OTEL_LOG_LEVEL, log_level)
        if log_level and log_level.upper() in log_levels:
            self.log_level = log_level.upper()
        logging.basicConfig(level=log_levels[self.log_level])

        self.traces_apikey = os.environ.get(
            HONEYCOMB_TRACES_APIKEY,
            os.environ.get(
                HONEYCOMB_API_KEY,
                (traces_apikey or apikey)
            )
        )
        self.metrics_apikey = os.environ.get(
            HONEYCOMB_METRICS_APIKEY,
            os.environ.get(
                HONEYCOMB_API_KEY,
                (metrics_apikey or apikey)
            )
        )

        self.service_name = os.environ.get(OTEL_SERVICE_NAME, service_name)
        if not self.service_name:
            # TODO - warn no service name set,
            # defaulting to unknown_service:python
            self.service_name = DEFAULT_SERVICE_NAME
        self.service_version = os.environ.get(
            OTEL_SERVICE_VERSION, service_version)

        self.traces_endpoint = os.environ.get(
            OTEL_EXPORTER_TRACES_ENDPOINT,
            os.environ.get(
                OTEL_EXPORTER_OTLP_ENDPOINT,
                (traces_endpoint or endpoint or DEFAULT_API_ENDPOINT)
            )
        )
        self.metrics_endpoint = os.environ.get(
            OTEL_EXPORTER_METRICS_ENDPOINT,
            os.environ.get(
                OTEL_EXPORTER_OTLP_ENDPOINT,
                (metrics_endpoint or endpoint or DEFAULT_API_ENDPOINT)
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

        endpoint_insecure_str = os.environ.get(
            OTEL_EXPORTER_OTLP_INSECURE, None)
        if endpoint_insecure_str:
            try:
                endpoint_insecure = bool(endpoint_insecure_str)
            except ValueError:
                _logger.warning(
                    "Unable to parse bool from OTEL_EXPORTER_OTLP_INSECURE. Defaulting to False.")

        traces_endpoint_insecure_str = os.getenv(
            OTEL_EXPORTER_OTLP_TRACES_INSECURE, endpoint_insecure_str)
        if traces_endpoint_insecure_str:
            try:
                self.traces_endpoint_insecure = bool(
                    traces_endpoint_insecure_str)
            except ValueError:
                _logger.warning(
                    "Unable to parse bool from OTEL_EXPORTER_OTLP_TRACES_INSECURE. Defaulting to False.")
        else:
            self.traces_endpoint_insecure = (
                traces_endpoint_insecure or endpoint_insecure)

        metrics_endpoint_insecure_str = os.getenv(
            OTEL_EXPORTER_OTLP_METRICS_INSECURE, endpoint_insecure_str)
        if metrics_endpoint_insecure_str:
            try:
                self.metrics_endpoint_insecure = bool(
                    metrics_endpoint_insecure_str)
            except ValueError:
                _logger.warning(
                    "Unable to parse bool from OTEL_EXPORTER_OTLP_METRICS_INSECURE. Defaulting to False.")
        else:
            self.metrics_endpoint_insecure = (
                metrics_endpoint_insecure or endpoint_insecure)

        self.dataset = os.environ.get(
            HONEYCOMB_DATASET, dataset)
        self.metrics_dataset = os.environ.get(
            HONEYCOMB_METRICS_DATASET, metrics_dataset)

    def get_traces_apikey(self):
        return self.traces_apikey

    def get_metrics_apikey(self):
        return self.metrics_apikey

    def get_traces_endpoint(self):
        return self.traces_endpoint

    def get_metrics_endpoint(self):
        return self.metrics_endpoint

    def get_trace_endpoint_credentials(self):
        if self.traces_endpoint_insecure:
            return None
        return ssl_channel_credentials()

    def get_metrics_endpoint_credentials(self):
        if self.metrics_endpoint_insecure:
            return None
        return ssl_channel_credentials()

    def get_trace_headers(self):
        headers = {
            "x-honeycomb-team": self.get_traces_apikey(),
        }
        if self.dataset and is_clasic(self.traces_apikey):
            headers["x-honeycomb-dataset"] = self.dataset
        return headers

    def get_metrics_headers(self):
        headers = {
            "x-honeycomb-team": self.get_metrics_apikey()
        }
        if self.metrics_dataset:
            headers["x-honeycomb-dataset"] = self.metrics_dataset
        return headers
