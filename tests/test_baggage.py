from opentelemetry.sdk.trace.export import SpanProcessor
from opentelemetry.trace import (
    NoOpTracer,
    Span,
    Tracer
)
from opentelemetry.baggage import (
    get_all,
    get_baggage,
    set_baggage
)
from opentelemetry.context import attach, detach
from honeycomb.opentelemetry.baggage import BaggageSpanProcessor

def test_check_the_baggage():
    baggageProcessor = BaggageSpanProcessor()
    assert isinstance(baggageProcessor, SpanProcessor)

def test_set_baggage_with_explicit_context():
    assert get_all() == {}
    ctx = set_baggage("worker", "bees")
    assert get_baggage("worker", context=ctx), "bees"

def test_set_baggage_with_token_using_token_attach():
    assert get_all() == {}
    token = attach(set_baggage("honey", "bee"))
    assert get_baggage("honey") == "bee"
    detach(token)
    assert get_baggage("honey") is None

def test_set_baggage_attaches_to_child_spans_and_detaches_properly():
    tracer = NoOpTracer()
    assert isinstance(tracer, Tracer)
    assert get_all() == {}
    honey_token = attach(set_baggage("bumble", "bee"))
    assert get_all() == {"bumble": "bee"}
    with tracer.start_as_current_span("hey") as span:
        assert isinstance(span, Span)
        assert get_all() == {"bumble": "bee"}
        moar_token = attach(set_baggage("moar", "bee"))
        assert get_all() == {"bumble": "bee", "moar": "bee"}
        with tracer.start_as_current_span("child") as child_span:
            assert isinstance(child_span, Span)
            assert get_all() == {"bumble": "bee", "moar": "bee"}
        detach(moar_token)
        detach(honey_token)
        assert get_all() == {}
