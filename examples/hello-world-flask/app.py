from flask import Flask
from opentelemetry import trace
# from honeycomb.opentelemetry import configure_opentelemetry, HoneycombOptions

# configure_opentelemetry(HoneycombOptions(debug=True, apikey="abc123", service_name="otel-python-example"))

# or use environment variables
# export HONEYCOMB_API_KEY=abc123
# export OTEL_SERVICE_NAME=otel-python-example

app = Flask(__name__)
tracer = trace.get_tracer(__name__)

@app.route("/")
def hello_world():
    with tracer.start_as_current_span("foo"):
        with tracer.start_as_current_span("bar"):
            print("baz")
    return "Hello World"
