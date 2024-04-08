# hello-world

This Python app returns "Hello World". This app uses the standard OpenTelemetry library to set up OpenTelemetry to export data to Honeycomb through configuration options set in the app's code. It is also possible to set configuration options through the `opentelemetry_instrument` command (see the [flask app](../hello-world-flask/README.md) as an example).

## Prerequisites

You'll also need [Poetry](https://python-poetry.org/) installed to run the example. Poetry automatically creates a virtual environment to run the example in so you don't need to manage one yourself.

## Running the example

Install the dependencies:

```bash
poetry install
```

Run the application:

```bash
poetry run python3 app.py
```

The app will output `Hello World` and then exit.

This app will send traces to local console with the configured `debug=True`.

To enable local visualizations:

```bash
export HONEYCOMB_ENABLE_LOCAL_VISUALIZATIONS=1
poetry run python3 app.py
```

To send to Honeycomb, set the API Key:

```bash
export OTEL_SERVICE_NAME=distroless-example
export OTEL_EXPORTER_OTLP_HEADERS="x-honeycomb-team=XXXX"
export OTEL_EXPORTER_OTLP_ENDPOINT=https://api.honeycomb.io:443
poetry run python3 app.py
```

You can configure exporter protocol with this flag:
`OTEL_EXPORTER_OTLP_PROTOCOL=grpc` or `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf`
