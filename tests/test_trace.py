from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as GRPCSpanExporter
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HTTPSpanExporter
)
from honeycomb.opentelemetry.baggage import BaggageSpanProcessor
from honeycomb.opentelemetry.local_exporter import LocalTraceLinkSpanExporter
from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.trace import create_tracer_provider

"""
Our Tracer Provider expects a series of span processors.

BaggageSpanProcessor (no export)
BatchSpanProcessor (Honeycomb Exporter)
SimpleSpanProcessor (Console Exporter)
SimpleSpanProcessor (Local Vis Exporter)

"""


def test_returns_tracer_provider_with_batch_and_baggage_span_processors():
    options = HoneycombOptions()
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)

    active_span_processors = tracer_provider._active_span_processor._span_processors
    assert len(active_span_processors) == 2
    assert any(
        isinstance(span_processor, BaggageSpanProcessor)
        for span_processor in active_span_processors
        )
    assert any(
        isinstance(span_processor, BatchSpanProcessor)
        for span_processor in active_span_processors
        )


def test_grpc_protocol_configures_grpc_span_exporter_on_batch_span_processor():
    options = HoneycombOptions(traces_exporter_protocol="grpc")
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)

    active_span_processors = tracer_provider._active_span_processor._span_processors
    assert len(active_span_processors) == 2
    (baggage, batch) = active_span_processors
    assert isinstance(batch, BatchSpanProcessor)
    assert isinstance(batch.span_exporter, GRPCSpanExporter)


def test_http_protocol_configures_http_span_exporter_on_batch_span_processor():
    options = HoneycombOptions(traces_exporter_protocol="http/protobuf")
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)

    active_span_processors = tracer_provider._active_span_processor._span_processors
    assert len(active_span_processors) == 2
    (baggage, batch) = active_span_processors
    assert isinstance(batch, BatchSpanProcessor)
    assert isinstance(batch.span_exporter, HTTPSpanExporter)


def test_setting_debug_addings_console_exporter_on_simple_span_processor():
    options = HoneycombOptions(debug=True)
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)

    active_span_processors = tracer_provider._active_span_processor._span_processors
    assert len(active_span_processors) == 3

    (baggage, batch, console) = active_span_processors
    assert isinstance(console, SimpleSpanProcessor)
    assert isinstance(console.span_exporter, ConsoleSpanExporter)


def test_setting_enable_local_visualizations_adds_local_trace_exporter_on_simple():
    options = HoneycombOptions(enable_local_visualizations=True)
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)

    active_span_processors = tracer_provider._active_span_processor._span_processors
    assert len(active_span_processors) == 3

    (baggage, batch, visualization) = active_span_processors
    assert isinstance(visualization, SimpleSpanProcessor)
    assert isinstance(visualization.span_exporter, LocalTraceLinkSpanExporter)


def test_setting_both_flags_enables_all_available_exporters():
    options = HoneycombOptions(enable_local_visualizations=True, debug=True)
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)

    active_span_processors = tracer_provider._active_span_processor._span_processors
    assert len(active_span_processors) == 4
