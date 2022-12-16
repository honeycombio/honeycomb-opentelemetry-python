from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter
)
from honeycomb.opentelemetry.options import HoneycombOptions


def create_tracer_provider(options: HoneycombOptions, resource: Resource):
    """
    Configures and returns a new TracerProvider to send traces telemetry.

    Args:
        options (HoneycombOptions): the Honeycomb options to configure with
        resource (Resource): the resource to use with the new tracer provider

    Returns:
        MeterProvider: the new tracer provider
    """
    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint=options.get_traces_endpoint(),
                credentials=options.get_trace_endpoint_credentials(),
                headers=options.get_trace_headers()
            )
        )
    )
    return trace_provider
