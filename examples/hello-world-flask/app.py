from flask import Flask
from opentelemetry import trace
from src.honeycomb.opentelemetry import hello
# todo: how to not include the src in imports /
# is this because a local dep? or bc the parent pyproject.toml config?

app = Flask(__name__)


@app.route("/")
def hello_world():
    with trace.get_tracer(__name__).start_as_current_span("foo"):
        with trace.get_tracer(__name__).start_as_current_span("bar"):
            print("baz")
    return hello.hello_world()
