from flask import Flask
from opentelemetry import trace

app = Flask(__name__)
tracer = trace.get_tracer(__name__)

@app.route("/")
def hello_world():
    with tracer.start_as_current_span("foo"):
        with tracer.start_as_current_span("bar"):
            print("baz")
    return "Hello World"
