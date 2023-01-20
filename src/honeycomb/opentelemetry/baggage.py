from opentelemetry.sdk.trace.export import BatchSpanProcessor

class BatchWithBaggageSpanProcessor(BatchSpanProcessor):
    # https://opentelemetry-python.readthedocs.io/en/latest/sdk/trace.export.html#opentelemetry.sdk.trace.export.BatchSpanProcessor
    """
    A span processor that behaves like a BatchSpanProcessor with the
    addition of BaggageSpanProcessor behavior.
    """

    def __init__(self, exporter) -> None:
        super().__init__(exporter)

    # TODO: BaggageSpanProcessor on start? 
    # a span being started
    # parent context in which the span was started
