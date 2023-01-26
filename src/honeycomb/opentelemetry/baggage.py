from opentelemetry import baggage
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.trace import Span
from opentelemetry.context import Context


class BaggageSpanProcessor(SimpleSpanProcessor):
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
        span: Span,
        parent_context: Context
    ) -> None:
        stuff = baggage.get_all(parent_context)
        for key, value in stuff.items():
            span.set_attribute(key, value)

    # https://opentelemetry.io/docs/instrumentation/python/cookbook/#capturing-baggage-at-different-contexts
    # TODO: propagate baggage from parent context
    #  get all entries
    # https://opentelemetry-python.readthedocs.io/en/latest/api/baggage.html#opentelemetry.baggage.get_all
    # for each entry, set them as span attributes
