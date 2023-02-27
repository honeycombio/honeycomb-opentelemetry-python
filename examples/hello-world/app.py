import os
from opentelemetry import trace
from honeycomb.opentelemetry import configure_opentelemetry, HoneycombOptions

configure_opentelemetry(
    HoneycombOptions(
        debug=True, # prints exported traces & metrics to the console, useful for debugging and setting up
        apikey=os.getenv("HONEYCOMB_API_KEY"), # Honeycomb API Key, required to send data to Honeycomb
        service_name="otel-python-example", # Dataset that will be populated with data from this service in Honeycomb
        enable_local_visualizations=True, # Will print a link to a trace produced in Honeycomb to the console, useful for debugging
        # traces_apikey = None, Set a specific Honeycomb API key just for traces
        # metrics_apikey = None, Set a specific Honeycomb API key just for metrics
        # service_version = None, Set a version for this service, will show up as an attribute on all spans
        # traces_endpoint = None, Set a specific exporter endpoint just for traces
        # metrics_endpoint = None, Set a specific exporter endpoint just for metrics
        # exporter_protocol = "grpc", Set the exporter protocol, grpc or http/protobuf
        # traces_exporter_protocol = "grpc", Set a specific exporter protocol just for traces, grpc or http/protobuf
        # metrics_exporter_protocol = "grpc", Set a specific exporter protocol just for metrics, grpc or http/protobuf
        # sample_rate = DEFAULT_SAMPLE_RATE, Set a sample rate for spans
        # metrics_dataset = None, Set a metrics dataset to enable metrics
    )
)

# or use environment variables instead of configure_opentelemetry
# export DEBUG=true
# export HONEYCOMB_API_KEY=abc123
# export OTEL_SERVICE_NAME=otel-python-example

tracer = trace.get_tracer("hello_world")

def hello_world():
    with tracer.start_as_current_span("hello"):
        with tracer.start_as_current_span("world"):
            print("Hello World")
    return "Hello World"

hello_world()
