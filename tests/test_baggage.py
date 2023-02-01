from opentelemetry.sdk.trace.export import SpanProcessor
from opentelemetry.trace import (
    Span,
    Tracer
)
from opentelemetry.baggage import (
    get_all as get_all_baggage,
    set_baggage
)
from opentelemetry.context import attach, detach
from honeycomb.opentelemetry.baggage import BaggageSpanProcessor
from honeycomb.opentelemetry.options import HoneycombOptions
from honeycomb.opentelemetry.resource import create_resource
from honeycomb.opentelemetry.trace import create_tracer_provider


def test_check_the_baggage():
    baggageProcessor = BaggageSpanProcessor()
    assert isinstance(baggageProcessor, SpanProcessor)


def test_set_baggage_attaches_to_child_spans_and_detaches_properly_with_context():
    options = HoneycombOptions()
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)

    # tracer has no baggage to start
    tracer = tracer_provider.get_tracer("my-tracer")
    assert isinstance(tracer, Tracer)
    assert get_all_baggage() == {}
    # set baggage in context
    ctx = set_baggage("queen", "bee")
    with tracer.start_as_current_span(name="bumble", context=ctx) as bumble_span:
        # span should have baggage key-value pair in context
        assert get_all_baggage(ctx) == {"queen": "bee"}
        # span should have baggage key-value pair in attribute
        assert bumble_span._attributes["queen"] == "bee"
        with tracer.start_as_current_span(name="child_span", context=ctx) as child_span:
            assert isinstance(child_span, Span)
            # child span should have baggage key-value pair in context
            assert get_all_baggage(ctx) == {"queen": "bee"}
            # child span should have baggage key-value pair in attribute
            assert child_span._attributes["queen"] == "bee"


def test_set_baggage_attaches_to_child_spans_and_detaches_properly_with_token():
    options = HoneycombOptions()
    resource = create_resource(options)
    tracer_provider = create_tracer_provider(options, resource)

    # tracer has no baggage to start
    tracer = tracer_provider.get_tracer("my-tracer")
    assert isinstance(tracer, Tracer)
    assert get_all_baggage() == {}
    # create a context token and set baggage
    honey_token = attach(set_baggage("bumble", "bee"))
    assert get_all_baggage() == {"bumble": "bee"}
    # in a new span, ensure the baggage is there
    with tracer.start_as_current_span("parent") as span:
        assert get_all_baggage() == {"bumble": "bee"}
        assert span._attributes["bumble"] == "bee"
        # create a second context token and set more baggage
        moar_token = attach(set_baggage("moar", "bee"))
        assert get_all_baggage() == {"bumble": "bee", "moar": "bee"}
        # in a child span, ensure all baggage is there as attributes
        with tracer.start_as_current_span("child") as child_span:
            assert get_all_baggage() == {"bumble": "bee", "moar": "bee"}
            assert child_span._attributes["bumble"] == "bee"
            assert child_span._attributes["moar"] == "bee"
        detach(moar_token)
    detach(honey_token)
    assert get_all_baggage() == {}
