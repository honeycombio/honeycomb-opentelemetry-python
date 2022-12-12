from honeycomb.opentelemetry.options import HoneycombOptions
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter


def create_meter_provider(options: HoneycombOptions, resource: Resource):
    exporter = OTLPMetricExporter(
        endpoint=options.endpoint,
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
