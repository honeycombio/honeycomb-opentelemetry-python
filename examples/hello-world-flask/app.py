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
                
        # compare current context to the root ctx that was passed in


        parent_ctx = baggage.set_baggage("context", "parent", root_ctx)

        # some more business logic here
        parent_ctx2 = baggage.set_baggage("additional_context", "parent", parent_ctx)
        
        
        with tracer.start_as_current_span(name="bar", context=parent_ctx2):
            child_ctx = baggage.set_baggage("context", "child") # this goes nowhere?
            print("baz")
    return "Hello World"