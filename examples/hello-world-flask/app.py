from flask import Flask
from opentelemetry import trace
from honeycomb.opentelemetry import hello

app = Flask(__name__)


@app.route("/")
def hello_world():
    with trace.get_tracer(__name__).start_as_current_span("foo"):
        with trace.get_tracer(__name__).start_as_current_span("bar"):
            print("baz")
    return hello.hello_world()
