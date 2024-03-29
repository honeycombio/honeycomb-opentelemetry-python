from typing import Optional
from opentelemetry.baggage import get_all as get_all_baggage
from opentelemetry.sdk.trace.export import SpanProcessor
from opentelemetry.trace import Span
from opentelemetry.context import Context


class BaggageSpanProcessor(SpanProcessor):
    """
     The BaggageSpanProcessor reads entries stored in Baggage
     from the parent context and adds the baggage entries' keys and
     values to the span as attributes on span start.

     Add this span processor to a tracer provider.

     Keys and values added to Baggage will appear on subsequent child
     spans for a trace within this service *and* be propagated to external
     services in accordance with any configured propagation formats
     configured. If the external services also have a Baggage span
     processor, the keys and values will appear in those child spans as
     well.

     ⚠ Warning ⚠️

     Do not put sensitive information in Baggage.

     To repeat: a consequence of adding data to Baggage is that the keys and
     values will appear in all outgoing HTTP headers from the application.

    """

    def __init__(self) -> None:
        pass

    def on_start(
        self,
        span: "Span",
        parent_context: Optional[Context] = None
    ) -> None:
        baggage = get_all_baggage(parent_context)
        for key, value in baggage.items():
            span.set_attribute(key, value)
