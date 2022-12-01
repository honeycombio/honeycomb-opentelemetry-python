# hello-world-flask

This simple Flask app that returns "Hello World".

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

## Upstream Distro Instrumentation Example (Replace with HNY Distro as we build it out, this is just to sandbox with the baseDistro for now!)

To send traces to local console:

```bash
$ poetry run opentelemetry-instrument --traces_exporter console --metrics_exporter console flask run
```

To send to Honeycomb: 

```bash
OTEL_EXPORTER_OTLP_HEADERS="x-honeycomb-team=your-api-key" OTEL_SERVICE_NAME="your-service-name" OTEL_EXPORTER_OTLP_ENDPOINT="api.honeycomb.io:443" poetry run opentelemetry-instrument flask run
```

Note: a Metrics-enabled Team API key is required for Honeycomb to receive metrics, if not available try including the `--metrics_exporter console` flag for opentelemetry-instrument above to see them locally instead

## Local Development - HelloWorld Import Example
If you make changes in the package's pyproject.toml you may need to run `poetry build` for the changes to take effect

If you make changes in python files in src/honeycomb/opentelemetry, with this setup the changes should propagate to this example app upon save.