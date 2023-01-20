import os
from flask import Flask
from opentelemetry import trace, baggage

# use environment variables
# export HONEYCOMB_API_KEY=abc123
# export OTEL_SERVICE_NAME=otel-python-example

app = Flask(__name__)
tracer = trace.get_tracer(__name__)

@app.route("/")
def hello_world():
    root_ctx = baggage.set_baggage("whatever", "friend")
    with tracer.start_as_current_span(name="foo", context=root_ctx):
        parent_ctx = baggage.set_baggage("context", "parent")
        with tracer.start_as_current_span(name="bar", context=parent_ctx):
            child_ctx = baggage.set_baggage("context", "child") # this goes nowhere?
            print("baz")
    return "Hello World"