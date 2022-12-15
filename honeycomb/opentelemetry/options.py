import logging
import os
from opentelemetry.sdk.environment_variables import (
    OTEL_EXPORTER_OTLP_ENDPOINT,
    OTEL_EXPORTER_OTLP_INSECURE,
    OTEL_EXPORTER_OTLP_METRICS_ENDPOINT,
    OTEL_EXPORTER_OTLP_METRICS_INSECURE,
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
    OTEL_EXPORTER_OTLP_TRACES_INSECURE,
    OTEL_LOG_LEVEL,
    OTEL_SERVICE_NAME
)
from grpc import ssl_channel_credentials

DEBUG = "DEBUG"
DEFAULT_API_ENDPOINT = "api.honeycomb.io:443"
DEFAULT_SERVICE_NAME = "unknown_service:python"
DEFAULT_LOG_LEVEL = "ERROR"
DEFAULT_SAMPLE_RATE = 1
HONEYCOMB_API_KEY = "HONEYCOMB_API_KEY"
HONEYCOMB_DATASET = "HONEYCOMB_DATASET"
HONEYCOMB_ENABLE_LOCAL_VISUALIZATIONS = "HONEYCOMB_ENABLE_LOCAL_VISUALIZATIONS"
HONEYCOMB_METRICS_APIKEY = "HONEYCOMB_METRICS_APIKEY"
HONEYCOMB_METRICS_DATASET = "HONEYCOMB_METRICS_DATASET"
HONEYCOMB_TRACES_APIKEY = "HONEYCOMB_TRACES_APIKEY"
INVALID_DEBUG_ERROR = "Unable to parse DEBUG environment variable. " + \
    "Defaulting to False."
INVALID_INSECURE_ERROR = "Unable to parse " + \
    "OTEL_EXPORTER_OTLP_INSECURE. Defaulting to False."
INVALID_LOCAL_VIS_ERROR = "Unable to parse " + \
    "HONEYCOMB_ENABLE_LOCAL_VISUALIZATIONS environment variable. " + \
    "Defaulting to false."
INVALID_METRICS_INSECURE_ERROR = "Unable to parse " + \
    "OTEL_EXPORTER_OTLP_METRICS_INSECURE. Defaulting to False."
INVALID_TRACES_INSECURE_ERROR = "Unable to parse " + \
    "OTEL_EXPORTER_OTLP_TRACES_INSECURE. Defaulting to False."
INVALID_SAMPLE_RATE_ERROR = "Unable to parse SAMPLE_RATE. " + \
    "Using sample rate of 1."
# not currently supported in OTel SDK, open PR:
# https://github.com/open-telemetry/opentelemetry-specification/issues/1901
OTEL_SERVICE_VERSION = "OTEL_SERVICE_VERSION"
SAMPLE_RATE = "SAMPLE_RATE"

log_levels = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

_logger = logging.getLogger(__name__)


def is_classic(apikey: str):
    return apikey and len(apikey) == 32


def parse_bool(environment_variable: str,
               default_value: bool,
               error_message: str):
    val = os.getenv(environment_variable, None)
    if val:
        try:
            return bool(val)
        except ValueError:
            _logger.warning(error_message)
    return default_value


def parse_int(environment_variable: str,
              default_value: int,
              error_message: str):
    val = os.getenv(environment_variable, None)
    if val:
        try:
            return int(val)
        except ValueError:
            _logger.warning(error_message)
    return default_value


class HoneycombOptions:
    """
    Honeycomb Options used to configure the OpenTelemetry SDK.

    Setting the debug flag enables verbose logging and sets the OTEL_LOG_LEVEL
    to DEBUG.
    """

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
    enable_local_visualizations = False

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
        metrics_dataset: str = None,
        enable_local_visualizations: bool = False
    ):
        self.debug = parse_bool(
            DEBUG,
            (debug or False),
            INVALID_DEBUG_ERROR
        )
        if self.debug:
            self.log_level = "DEBUG"
        else:
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
            OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
            os.environ.get(
                OTEL_EXPORTER_OTLP_ENDPOINT,
                (traces_endpoint or endpoint or DEFAULT_API_ENDPOINT)
            )
        )
        self.metrics_endpoint = os.environ.get(
            OTEL_EXPORTER_OTLP_METRICS_ENDPOINT,
            os.environ.get(
                OTEL_EXPORTER_OTLP_ENDPOINT,
                (metrics_endpoint or endpoint or DEFAULT_API_ENDPOINT)
            )
        )

        self.sample_rate = parse_int(
            SAMPLE_RATE,
            (sample_rate or DEFAULT_SAMPLE_RATE),
            INVALID_SAMPLE_RATE_ERROR
        )

        endpoint_insecure = parse_bool(
            OTEL_EXPORTER_OTLP_INSECURE,
            (endpoint_insecure or False),
            INVALID_INSECURE_ERROR
        )
        self.traces_endpoint_insecure = parse_bool(
            OTEL_EXPORTER_OTLP_TRACES_INSECURE,
            (traces_endpoint_insecure or endpoint_insecure),
            INVALID_TRACES_INSECURE_ERROR
        )
        self.metrics_endpoint_insecure = parse_bool(
            OTEL_EXPORTER_OTLP_METRICS_INSECURE,
            (metrics_endpoint_insecure or endpoint_insecure),
            INVALID_METRICS_INSECURE_ERROR
        )

        self.dataset = os.environ.get(
            HONEYCOMB_DATASET, dataset)
        self.metrics_dataset = os.environ.get(
            HONEYCOMB_METRICS_DATASET, metrics_dataset)

        self.enable_local_visualizations = parse_bool(
            HONEYCOMB_ENABLE_LOCAL_VISUALIZATIONS,
            enable_local_visualizations,
            INVALID_LOCAL_VIS_ERROR
        )

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
            "x-honeycomb-team": self.traces_apikey,
        }
        if self.dataset and is_classic(self.traces_apikey):
            headers["x-honeycomb-dataset"] = self.dataset
        return headers

    def get_metrics_headers(self):
        headers = {
            "x-honeycomb-team": self.metrics_apikey
        }
        if self.metrics_dataset:
            headers["x-honeycomb-dataset"] = self.metrics_dataset
        return headers
