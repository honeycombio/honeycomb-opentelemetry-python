# hello-world-flask

This simple Flask app that returns "Hello World". This app configures OpenTelemetry to send data to Honeycomb through environment variables. It also contains an example of sending metrics with OpenTelemetry.

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

For local export right now

```bash
DEBUG=TRUE poetry run opentelemetry-instrument flask run
```

To send to Honeycomb:

```bash
HONEYCOMB_API_KEY="your-api-key" OTEL_SERVICE_NAME="your-service-name" poetry run opentelemetry-instrument flask run
```

You can configure exporter protocol with this flag:
`OTEL_EXPORTER_OTLP_PROTOCOL=grpc` or `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf`

If you make changes in the package's pyproject.toml you may need to run `poetry build` for the changes to take effect

If you make changes in python files in src/honeycomb/opentelemetry, with this setup the changes should propagate to this example app upon save.