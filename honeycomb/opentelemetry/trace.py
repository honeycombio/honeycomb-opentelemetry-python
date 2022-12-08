from honeycomb.opentelemetry.options import HoneycombOptions
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from grpc import ssl_channel_credentials


def create_span_exporter(options: HoneycombOptions):
    if options.insecure:
        credentials = None
    else:
        credentials = ssl_channel_credentials()
    return OTLPSpanExporter(
        endpoint=options.endpoint,
        credentials=credentials,
        headers={
            "x-honeycomb-team": options.apikey
        },
    )
