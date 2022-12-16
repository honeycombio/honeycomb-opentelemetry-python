from honeycomb.opentelemetry.local_exporter import LocalTraceLinkSpanExporter
from honeycomb.opentelemetry.options import HoneycombOptions
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
    ConsoleSpanExporter
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as GRPCSpanExporter
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HTTPSpanExporter
)


def create_tracer_provider(options: HoneycombOptions, resource: Resource):
    if options.traces_exporter_protocol == "grpc":
        exporter = GRPCSpanExporter(
            endpoint=options.get_traces_endpoint(),
            credentials=options.get_trace_endpoint_credentials(),
            headers=options.get_trace_headers()
        )
    else:
        exporter = HTTPSpanExporter(
            endpoint=options.get_traces_endpoint(),
            headers=options.get_trace_headers()
        )
    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(
        BatchSpanProcessor(
            exporter
        )
    )
    if options.debug:
        trace_provider.add_span_processor(
            SimpleSpanProcessor(
                ConsoleSpanExporter()
            )
        )
    if options.enable_local_visualizations:
        trace_provider.add_span_processor(
            SimpleSpanProcessor(
                LocalTraceLinkSpanExporter(options)
            )
        )
    return trace_provider
