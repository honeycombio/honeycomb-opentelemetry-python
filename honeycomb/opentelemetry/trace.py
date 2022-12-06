from honeycomb.opentelemetry.options import HoneycombOptions
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)


def create_tracer_provider(options: HoneycombOptions, resource: Resource):
    exporter = OTLPSpanExporter(
        endpoint=options.endpoint,
        insecure=options.insecure,
        headers={
            "x-honeycomb-team": options.apikey
        },
    )
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(
        BatchSpanProcessor(
            exporter
        )
    )
    return provider
