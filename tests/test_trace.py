from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as GRPCSpanExporter
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HTTPSpanExporter
)
from honeycomb.opentelemetry.local_exporter import LocalTraceLinkSpanExporter
from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.trace import create_tracer_provider


def test_returns_tracer_provider():
    options = HoneycombOptions()
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)
    assert isinstance(tracer_provider, TracerProvider)
    assert len(tracer_provider._active_span_processor._span_processors) == 1


def test_grpc_protocol_configures_grpc_span_exporter():
    options = HoneycombOptions(traces_exporter_protocol="grpc")
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)
    assert isinstance(
        tracer_provider._active_span_processor._span_processors[0].span_exporter, GRPCSpanExporter)
    assert len(tracer_provider._active_span_processor._span_processors) == 1


def test_http_protocol_configures_http_span_exporter():
    options = HoneycombOptions(traces_exporter_protocol="http/protobuf")
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)
    assert isinstance(
        tracer_provider._active_span_processor._span_processors[0].span_exporter, HTTPSpanExporter)
    assert len(tracer_provider._active_span_processor._span_processors) == 1


def test_setting_debug_addings_console_exporter():
    options = HoneycombOptions(debug=True)
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)
    assert len(tracer_provider._active_span_processor._span_processors) == 2
    assert isinstance(
        tracer_provider._active_span_processor._span_processors[1].span_exporter, ConsoleSpanExporter)


def test_setting_enable_local_visualizations_adds_local_trace_exporter():
    options = HoneycombOptions(enable_local_visualizations=True)
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)
    assert len(tracer_provider._active_span_processor._span_processors) == 2
    assert isinstance(
        tracer_provider._active_span_processor._span_processors[1].span_exporter, LocalTraceLinkSpanExporter)
