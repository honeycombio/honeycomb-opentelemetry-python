import os
from opentelemetry import trace, baggage, metrics
from opentelemetry.trace import set_tracer_provider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor
)
from opentelemetry.context import attach, detach
from honeycomb.opentelemetry.components.options import HoneycombOptions
from honeycomb.opentelemetry.components.resource import create_resource
from honeycomb.opentelemetry.components.local_exporter import LocalTraceLinkSpanExporter
from honeycomb.opentelemetry.components.sampler import configure_sampler
from honeycomb.opentelemetry.components.resource import create_resource
from honeycomb.opentelemetry.components.trace import create_tracer_provider
from honeycomb.opentelemetry.components.metrics import create_meter_provider


def configure_honeycomb_components():
    opts = HoneycombOptions()
    resource = create_resource(opts)
    set_tracer_provider(create_tracer_provider(opts, resource))

configure_honeycomb_components()

meter = metrics.get_meter("hello_world_meter")
sheep = meter.create_counter('sheep')

tracer = trace.get_tracer("hello_world_tracer")

def hello_world():
    token = attach(baggage.set_baggage(
        "baggy", "important_value"))
    with tracer.start_as_current_span(name="hello"):
        token_second = attach(baggage.set_baggage(
            "for_the_children", "another_important_value"))
        with tracer.start_as_current_span(name="world") as span:
            span.set_attribute("message", "hello world!")
            print("Hello World")
        detach(token_second)
    detach(token)
    sheep.add(1, {'app.route': '/'})
    return "Hello World"


hello_world()
