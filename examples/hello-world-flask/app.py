from flask import Flask
from opentelemetry import trace
# from honeycomb.opentelemetry import configure_opentelemetry
# from opentelemetry.instrumentation.flask import FlaskInstrumentor

# configure_opentelemetry()

app = Flask(__name__)
# FlaskInstrumentor().instrument_app(app)
tracer = trace.get_tracer(__name__)

@app.route("/")
def hello_world():
    with tracer.start_as_current_span("foo"):
        with tracer.start_as_current_span("bar"):
            print("baz")
    return "Hello World"
