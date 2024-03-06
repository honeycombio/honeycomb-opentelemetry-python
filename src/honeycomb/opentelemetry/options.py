import logging
import os
import re
from opentelemetry.sdk.environment_variables import (
    OTEL_EXPORTER_OTLP_ENDPOINT,
    OTEL_EXPORTER_OTLP_INSECURE,
    OTEL_EXPORTER_OTLP_METRICS_ENDPOINT,
    OTEL_EXPORTER_OTLP_METRICS_INSECURE,
    OTEL_EXPORTER_OTLP_METRICS_PROTOCOL,
    OTEL_EXPORTER_OTLP_PROTOCOL,
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
    OTEL_EXPORTER_OTLP_TRACES_INSECURE,
    OTEL_EXPORTER_OTLP_TRACES_PROTOCOL,
    OTEL_LOG_LEVEL,
    OTEL_SERVICE_NAME
)
from grpc import ssl_channel_credentials

# Environment Variable Names
OTEL_SERVICE_VERSION = "OTEL_SERVICE_VERSION"
DEBUG = "DEBUG"
HONEYCOMB_ENABLE_LOCAL_VISUALIZATIONS = "HONEYCOMB_ENABLE_LOCAL_VISUALIZATIONS"
SAMPLE_RATE = "SAMPLE_RATE"

# HNY Credential Names
HONEYCOMB_API_KEY = "HONEYCOMB_API_KEY"
HONEYCOMB_API_ENDPOINT = "HONEYCOMB_API_ENDPOINT"
HONEYCOMB_TRACES_APIKEY = "HONEYCOMB_TRACES_APIKEY"
HONEYCOMB_DATASET = "HONEYCOMB_DATASET"
HONEYCOMB_METRICS_APIKEY = "HONEYCOMB_METRICS_APIKEY"
HONEYCOMB_METRICS_DATASET = "HONEYCOMB_METRICS_DATASET"

# Default values
DEFAULT_API_ENDPOINT = "https://api.honeycomb.io:443"
DEFAULT_EXPORTER_PROTOCOL = "grpc"
DEFAULT_SERVICE_NAME = "unknown_service:python"
DEFAULT_LOG_LEVEL = "ERROR"
DEFAULT_SAMPLE_RATE = 1

# Errors and Warnings
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
INVALID_EXPORTER_PROTOCOL_ERROR = "Invalid OTLP exporter protocol " + \
    "detected. Must be one of ['grpc', 'http/protobuf']. Defaulting to grpc."
MISSING_API_KEY_ERROR = "Missing API key. Specify either " + \
    "HONEYCOMB_API_KEY environment variable or apikey in the options" + \
    "parameter."
MISSING_SERVICE_NAME_ERROR = "Missing service name. Specify either " + \
    "OTEL_SERVICE_NAME environment variable or service_name in the " + \
    "options parameter. If left unset, this will show up in Honeycomb " + \
    "as unknown_service:python"
MISSING_DATASET_ERROR = "Missing dataset. Specify either " + \
    "HONEYCOMB_DATASET environment variable or dataset in the options " + \
    "parameter."
IGNORED_DATASET_ERROR = "Dataset is ignored in favor of service name."
# not currently supported in OTel SDK, open PR:
# https://github.com/open-telemetry/opentelemetry-specification/issues/1901

log_levels = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

EXPORTER_PROTOCOL_GRPC = "grpc"
EXPORTER_PROTOCOL_HTTP_PROTO = "http/protobuf"

TRACES_HTTP_PATH = "v1/traces"
METRICS_HTTP_PATH = "v1/metrics"

exporter_protocols = {
    EXPORTER_PROTOCOL_GRPC,
    EXPORTER_PROTOCOL_HTTP_PROTO
}

_logger = logging.getLogger(__name__)


def is_classic(apikey: str) -> bool:
    """
    Determines whether the passed in API key is a classic API key or not.
    v1 Configuration API keys have 22 or 23 characters.
    v1 Classic Configuration API keys have 32 characters.
    v2 Ingest keys have 64 characters and a prefix of hcxik.
    v2 Classic Ingest keys have 64 characters and a prefix of hcxic.

    Returns:
        bool: true if the api key is a classic key, false if not
    """
    if not apikey:
        return False
    if re.match(r'^[a-f0-9]{32}$', apikey):
        return True
    if re.match(r'^hc[a-z]ic_[a-z0-9]{58}$', apikey):
        return True
    return False


def parse_bool(environment_variable: str,
               default_value: bool,
               error_message: str) -> bool:
    """
    Attempts to parse the provided environment variable into a bool. If it
    does not exist or fails parse, the default value is returned instead.

    Args:
        environment_variable (str): the environment variable name to use
        default_value (bool): the default value if not found or unable parse
        error_message (str): the error message to log if unable to parse

    Returns:
        bool: either the parsed environment variable or default value
    """
    val = os.getenv(environment_variable, None)
    if val:
        try:
            return bool(val)
        except ValueError:
            _logger.warning(error_message)
    return default_value


def parse_int(environment_variable: str,
              param: int,
              default_value: int,
              error_message: str) -> int:
    """
    Attempts to parse the provided environment variable into an int. If it
    does not exist or fails parse, the default value is returned instead.

    Args:
        environment_variable (str): the environment variable name to use
        param(int): fallback parameter to check before setting default
        default_value (int): the default value if not found or unable parse
        error_message (str): the error message to log if unable to parse

    Returns:
        int: either the parsed environment variable, param, or default value
    """
    val = os.getenv(environment_variable, None)
    if val:
        try:
            return int(val)
        except ValueError:
            _logger.warning(error_message)
            return default_value
    elif isinstance(param, int):
        return param
    else:
        return default_value


def _append_traces_path(protocol: str, endpoint: str) -> str:
    """
    Appends the OTLP traces HTTP path '/v1/traces' to the endpoint if the
    protocol is http/protobuf and it doesn't already exist.

    Returns:
        string: the endpoint, optionally appended with traces path
    """
    if endpoint and protocol == "http/protobuf" \
       and not endpoint.strip("/").endswith(TRACES_HTTP_PATH):
        return "/".join([endpoint.strip("/"), TRACES_HTTP_PATH])
    return endpoint


def _append_metrics_path(protocol: str, endpoint: str) -> str:
    """
    Appends the OTLP metrics HTTP path '/v1/metrics' to the endpoint if the
    protocol is http/protobuf and it doesn't already exist.

    Returns:
        string: the endpoint, optionally appended with metrics path
    """
    if endpoint and protocol == "http/protobuf" \
       and not endpoint.strip("/").endswith(METRICS_HTTP_PATH):
        return "/".join([endpoint.strip("/"), METRICS_HTTP_PATH])
    return endpoint


# pylint: disable=too-many-arguments,too-many-instance-attributes
class HoneycombOptions:
    """
    Honeycomb Options used to configure the OpenTelemetry SDK.

    Setting the debug flag TRUE enables verbose logging and sets the
    OTEL_LOG_LEVEL to DEBUG.

    An option set as an environment variable will override any existing
    options declared as parameter variables, if neither are present it
    will fall back to the default value.

    Defaults are declared at the top of this file, i.e. DEFAULT_SAMPLE_RATE = 1
    """
    traces_apikey = None
    metrics_apikey = None
    service_name = DEFAULT_SERVICE_NAME
    service_version = None
    endpoint = DEFAULT_API_ENDPOINT
    traces_endpoint = None
    metrics_endpoint = None
    traces_endpoint_insecure = False
    metrics_endpoint_insecure = False
    traces_exporter_protocol = DEFAULT_EXPORTER_PROTOCOL
    metrics_exporter_protocol = DEFAULT_EXPORTER_PROTOCOL
    sample_rate = DEFAULT_SAMPLE_RATE
    debug = False
    log_level = DEFAULT_LOG_LEVEL
    dataset = None
    metrics_dataset = None
    enable_local_visualizations = False

    # pylint: disable=too-many-locals,too-many-branches,too-many-statements
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
        enable_local_visualizations: bool = False,
        exporter_protocol: str = EXPORTER_PROTOCOL_GRPC,
        traces_exporter_protocol: str = None,
        metrics_exporter_protocol: str = None
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
        if not self.traces_apikey:
            _logger.warning(MISSING_API_KEY_ERROR)

        self.metrics_apikey = os.environ.get(
            HONEYCOMB_METRICS_APIKEY,
            os.environ.get(
                HONEYCOMB_API_KEY,
                (metrics_apikey or apikey)
            )
        )
        if not self.traces_apikey:
            _logger.warning(MISSING_API_KEY_ERROR)

        self.service_name = os.environ.get(OTEL_SERVICE_NAME, service_name)
        if not self.service_name:
            _logger.warning(MISSING_SERVICE_NAME_ERROR)
            self.service_name = DEFAULT_SERVICE_NAME
        self.service_version = os.environ.get(
            OTEL_SERVICE_VERSION, service_version)

        exporter_protocol = os.environ.get(
            OTEL_EXPORTER_OTLP_PROTOCOL,
            (exporter_protocol or DEFAULT_EXPORTER_PROTOCOL))
        if exporter_protocol not in exporter_protocols:
            _logger.warning(INVALID_EXPORTER_PROTOCOL_ERROR)
            exporter_protocol = DEFAULT_EXPORTER_PROTOCOL

        self.traces_exporter_protocol = os.environ.get(
            OTEL_EXPORTER_OTLP_TRACES_PROTOCOL,
            (traces_exporter_protocol or exporter_protocol))
        if traces_exporter_protocol and (
                traces_exporter_protocol not in exporter_protocols):
            _logger.warning(INVALID_EXPORTER_PROTOCOL_ERROR)
            self.traces_exporter_protocol = exporter_protocol

        self.metrics_exporter_protocol = os.environ.get(
            OTEL_EXPORTER_OTLP_METRICS_PROTOCOL,
            (metrics_exporter_protocol or exporter_protocol))
        if metrics_exporter_protocol and (
                metrics_exporter_protocol not in exporter_protocols):
            _logger.warning(INVALID_EXPORTER_PROTOCOL_ERROR)
            self.metrics_exporter_protocol = exporter_protocol

        self.endpoint = os.environ.get(
            HONEYCOMB_API_ENDPOINT,
            endpoint
        )

        if not self.endpoint:
            self.endpoint = DEFAULT_API_ENDPOINT

        self.traces_endpoint = os.environ.get(
            OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
            None
        )
        if not self.traces_endpoint:
            self.traces_endpoint = _append_traces_path(
                self.traces_exporter_protocol,
                os.environ.get(OTEL_EXPORTER_OTLP_ENDPOINT, None)
            )
            if not self.traces_endpoint:
                self.traces_endpoint = traces_endpoint
                if not self.traces_endpoint:
                    self.traces_endpoint = _append_traces_path(
                        self.traces_exporter_protocol,
                        self.endpoint
                    )

        # if http/protobuf protocol and using generic env or param
        # append /v1/metrics path
        self.metrics_endpoint = os.environ.get(
            OTEL_EXPORTER_OTLP_METRICS_ENDPOINT,
            None
        )
        if not self.metrics_endpoint:
            self.metrics_endpoint = _append_metrics_path(
                self.metrics_exporter_protocol,
                os.environ.get(OTEL_EXPORTER_OTLP_ENDPOINT, None)
            )
            if not self.metrics_endpoint:
                self.metrics_endpoint = metrics_endpoint
                if not self.metrics_endpoint:
                    self.metrics_endpoint = _append_metrics_path(
                        self.metrics_exporter_protocol,
                        self.endpoint
                    )

        self.sample_rate = parse_int(
            SAMPLE_RATE,
            sample_rate,
            DEFAULT_SAMPLE_RATE,
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
        if self.dataset and not is_classic(self.traces_apikey):
            _logger.warning(IGNORED_DATASET_ERROR)
        if not self.dataset and is_classic(self.traces_apikey):
            _logger.warning(MISSING_DATASET_ERROR)

        self.metrics_dataset = os.environ.get(
            HONEYCOMB_METRICS_DATASET, metrics_dataset)

        self.enable_local_visualizations = parse_bool(
            HONEYCOMB_ENABLE_LOCAL_VISUALIZATIONS,
            enable_local_visualizations,
            INVALID_LOCAL_VIS_ERROR
        )

    def get_traces_endpoint(self) -> str:
        """
        Returns the OTLP traces endpoint to send spans to.
        """
        return self.traces_endpoint

    def get_metrics_endpoint(self) -> str:
        """
        Returns the OTLP metrics endpoint to send metrics to.
        """
        return self.metrics_endpoint

    def get_trace_endpoint_credentials(self):
        """
        Get the grpc credentials to use when sending to the traces endpoint.
        """
        if self.traces_endpoint_insecure:
            return None
        return ssl_channel_credentials()

    def get_metrics_endpoint_credentials(self):
        """
        Get the grpc credentials to use when sending to the metrics endpoint.
        """
        if self.metrics_endpoint_insecure:
            return None
        return ssl_channel_credentials()

    def get_trace_headers(self):
        """
        Gets the headers to send traces telemetry.
        """
        headers = {
            "x-honeycomb-team": self.traces_apikey,
        }
        if self.dataset and is_classic(self.traces_apikey):
            headers["x-honeycomb-dataset"] = self.dataset
        return headers

    def get_metrics_headers(self):
        """
        Gets the headers to send metrics telemetry.
        """
        headers = {
            "x-honeycomb-team": self.metrics_apikey
        }
        if self.metrics_dataset:
            headers["x-honeycomb-dataset"] = self.metrics_dataset
        return headers
