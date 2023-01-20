from flask import Flask
from opentelemetry import trace, baggage

app = Flask(__name__)
tracer = trace.get_tracer(__name__)

@app.route("/")
def hello_world():
    with tracer.start_as_current_span(name="foo"):
        parent_ctx = baggage.set_baggage("context", "parent")
        with tracer.start_as_current_span(name="bar", context=parent_ctx):
            baggage.set_baggage("context", "child")
            print("baz")
    return "Hello World"