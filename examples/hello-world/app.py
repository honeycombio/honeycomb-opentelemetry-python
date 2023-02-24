import os
from opentelemetry import trace, baggage, metrics
from opentelemetry.context import attach, detach
from honeycomb.opentelemetry import configure_opentelemetry, HoneycombOptions

configure_opentelemetry(
    HoneycombOptions(
        debug=True, # prints exported traces & metrics to the console, useful for debugging and setting up
        apikey=os.getenv("HONEYCOMB_API_KEY"), # Honeycomb API Key, required to send data to Honeycomb
        service_name="otel-python-example", # Dataset that will be populated with data from this service in Honeycomb
        # enable_local_visualizations=True, # Will print a link to a trace produced in Honeycomb to the console, useful for debugging
        # traces_apikey = None, Set a specific Honeycomb API key just for traces
        # metrics_apikey = None, Set a specific Honeycomb API key just for metrics
        # service_version = None, Set a version for this service, will show up as an attribute on all spans
        endpoint=os.getenv("HONEYCOMB_API_ENDPOINT",
                           None),  # set specific endpoint if not Honeycomb default
        endpoint_insecure=os.getenv(
            "OTEL_EXPORTER_OTLP_INSECURE", None),  # default is False; set to True if setting insecure endpoint
        # traces_endpoint = None, Set a specific exporter endpoint just for traces
        # metrics_endpoint = None, Set a specific exporter endpoint just for metrics
        # Set the exporter protocol, grpc or http/protobuf
        exporter_protocol=os.getenv("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc"),
        # traces_exporter_protocol = "grpc", Set a specific exporter protocol just for traces, grpc or http/protobuf
        # metrics_exporter_protocol = "grpc", Set a specific exporter protocol just for metrics, grpc or http/protobuf
        # sample_rate = DEFAULT_SAMPLE_RATE, Set a sample rate for spans
        # Set a metrics dataset to enable metrics
        metrics_dataset=os.getenv("HONEYCOMB_METRICS_DATASET", None),
    )
)

# or use environment variables instead of configure_opentelemetry
# export DEBUG=true
# export HONEYCOMB_API_KEY=abc123
# export OTEL_SERVICE_NAME=otel-python-example

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
