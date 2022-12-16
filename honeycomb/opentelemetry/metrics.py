from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter
)
from honeycomb.opentelemetry.options import HoneycombOptions


def create_meter_provider(options: HoneycombOptions, resource: Resource):
    """
    Configures and returns a new MeterProvider to send metrics telemetry.

    Args:
        options (HoneycombOptions): the Honeycomb options to configure with
        resource (Resource): the resource to use with the new meter provider

    Returns:
        MeterProvider: the new meter provider
    """
    exporter = OTLPMetricExporter(
        endpoint=options.get_metrics_endpoint(),
        credentials=options.get_metrics_endpoint_credentials(),
        headers=options.get_metrics_headers()
    )
    reader = PeriodicExportingMetricReader(
        exporter,
        export_timeout_millis=10000  # TODO set via OTEL env var
    )
    return MeterProvider(
        metric_readers=[reader],
        resource=resource
    )
