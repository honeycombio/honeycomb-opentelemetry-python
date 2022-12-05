from honeycomb.opentelemetry.options import HoneycombOptions
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter,
)


def create_meter_provider(options: HoneycombOptions, resource: Resource):
    exporter = OTLPMetricExporter()
    meter_readers = {}
    return MeterProvider(meter_readers, resource)
