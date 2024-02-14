#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from honeycomb.opentelemetry import configure_opentelemetry, HoneycombOptions

configure_opentelemetry(
    HoneycombOptions(
        debug=True,  # prints exported traces & metrics to the console, useful for debugging and setting up
        # Honeycomb API Key, required to send data to Honeycomb
        apikey=os.getenv("HONEYCOMB_API_KEY"),
        # Dataset that will be populated with data from this service in Honeycomb
        service_name="hello-world-django",
        # enable_local_visualizations=True, # Will print a link to a trace produced in Honeycomb to the console, useful for debugging
        # traces_apikey = None, Set a specific Honeycomb API key just for traces
        # metrics_apikey = None, Set a specific Honeycomb API key just for metrics
        # service_version = None, Set a version for this service, will show up as an attribute on all spans
        endpoint=os.getenv("HONEYCOMB_API_ENDPOINT",
                           None),  # set specific endpoint if not Honeycomb default
        endpoint_insecure=os.getenv(
            "OTEL_EXPORTER_OTLP_INSECURE", None),  # default is False; set to True if setting insecure endpoint
        # traces_endpoint = None, Set a specific exporter endpoint just for traces
        # metrics_endpoint = None, Set a specific exporter endpoint just for metrics
        # Set the exporter protocol, grpc or http/protobuf
        exporter_protocol=os.getenv("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc"),
        # traces_exporter_protocol = "grpc", Set a specific exporter protocol just for traces, grpc or http/protobuf
        # metrics_exporter_protocol = "grpc", Set a specific exporter protocol just for metrics, grpc or http/protobuf
        # sample_rate = DEFAULT_SAMPLE_RATE, Set a sample rate for spans
        # Set a metrics dataset to enable metrics
        metrics_dataset=os.getenv("HONEYCOMB_METRICS_DATASET", None),
    )
)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
