import os
from flask import Flask
from opentelemetry import trace, baggage, metrics
from opentelemetry.context import attach, detach

# use environment variables
# export HONEYCOMB_API_KEY=abc123
# export OTEL_SERVICE_NAME=otel-python-example
# export DEBUG=true
# HONEYCOMB_ENABLE_LOCAL_VISUALIZATIONS=true

# To enable metrics, set a metrics dataset
# export HONEYCOMB_METRICS_DATASET=otel-python-example-metrics

app = Flask(__name__)
# tracing
tracer = trace.get_tracer("hello_world_flask_tracer")
# metrics
meter = metrics.get_meter("hello_world_flask_meter")
bee_counter = meter.create_counter("bee_counter")


@app.route("/")
# Recommended: use attach and detach tokens for Context management with Baggage
def hello_world():
    # adding baggage attributes (key, value)
    token = attach(baggage.set_baggage("queen", "bee"))

    with tracer.start_as_current_span(name="honey") as span:

        # adding baggage attributes (key, value)
        token_honey = attach(baggage.set_baggage("honey", "bee"))
        # setting a span attribute directly (key, value)
        span.set_attribute("message", "hello world!")

        with tracer.start_as_current_span(name="child"):
            # this goes nowhere if it is the final span in a trace
            child_token = attach(
                baggage.set_baggage("bee", "that_maybe_doesnt_propagate")
            )
            detach(child_token)
        detach(token_honey)
    detach(token)
    # counter incremented by 1, attributes (route) associated with the increment
    bee_counter.add(1, {'app.route': '/'})
    return "Hello World"


@app.route("/ctx")
# For manually passing around the Context for baggage
def hello_ctx_world():
    ctx = baggage.set_baggage("worker", "bees")
    with tracer.start_as_current_span(name="bumble", context=ctx):
        ctx = baggage.set_baggage("bumble", "bees", ctx)
        # say you have more business logic before adding additional baggage
        ctx = baggage.set_baggage("additional", "bees", ctx)
        with tracer.start_as_current_span(name="last", context=ctx):
            # this goes nowhere if it is the final span in a trace
            ctx = baggage.set_baggage("last", "bee", ctx)
    bee_counter.add(1, {'app.route': '/ctx'})
    return "Hello Context World"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
