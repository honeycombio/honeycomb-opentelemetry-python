from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
    ConsoleMetricExporter
)
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter as GRPCMetricExporter
)
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter as HTTPMetricExporter
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
    if options.metrics_exporter_protocol == "grpc":
        exporter = GRPCMetricExporter(
            endpoint=options.get_metrics_endpoint(),
            credentials=options.get_metrics_endpoint_credentials(),
            headers=options.get_metrics_headers()
        )
    else:
        exporter = HTTPMetricExporter(
            endpoint=options.get_metrics_endpoint(),
            headers=options.get_metrics_headers()
        )
    readers = [
        PeriodicExportingMetricReader(
            exporter
        )
    ]
    if options.debug:
        readers.append(
            PeriodicExportingMetricReader(
                ConsoleMetricExporter(),
            )
        )
    return MeterProvider(
        metric_readers=readers,
        resource=resource
    )
