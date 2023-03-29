# hello-world-flask

This simple Flask app that returns "Hello World". This app configures OpenTelemetry to send data to Honeycomb using the `opentelemetry_instrument` command and environment variables.

It also contains examples of:

- sending metrics with OpenTelemetry using a counter
- using baggage with context tokens
- manually passing baggage with context
- setting a span attribute

If you are looking for an example using the `configure_opentelemetry()` function and parameters, check out [hello-world app](../hello-world/README.md).

## Prerequisites

You'll also need [Poetry](https://python-poetry.org/) installed to run the example. Poetry automatically creates a virtual environment to run the example in so you don't need to manage one yourself.

## Running the example

Install the dependencies:

```bash
poetry install
```

Run the application:

```bash
poetry run flask run
```

Now you can `curl` the app:

```bash
$ curl localhost:5000
Hello World
```

## Distro Instrumentation Example

To send traces to local console:

```bash
DEBUG=TRUE poetry run opentelemetry-instrument flask run
```

To send traces to Honeycomb:

```bash
HONEYCOMB_API_KEY="your-api-key" OTEL_SERVICE_NAME="your-service-name" poetry run opentelemetry-instrument flask run
```

To enable metrics, you will need to set a metrics dataset:
`HONEYCOMB_METRICS_DATASET=otel-python-example-metrics`

You can configure exporter protocol with this flag:
`OTEL_EXPORTER_OTLP_PROTOCOL=grpc` or `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf`
