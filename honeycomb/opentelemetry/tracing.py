from honeycomb.opentelemetry.options import HoneycombOptions
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)


def create_tracer_provider(options: HoneycombOptions, resource: Resource):
    exportor = OTLPSpanExporter()
    return TracerProvider(resource)
