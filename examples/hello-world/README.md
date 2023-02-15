# hello-world

This simple Python app returns "Hello World". This app uses the `configure_opentelemetry` method from `honeycomb.opentelemetry` to set up OpenTelemetry to export data to Honeycomb through configuration options set in the app's code. It is also possible to set configuration options through environment varaibles (see the [flask app](examples/hello-world-flask/README.md) as an example).

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

## Distro Instrumentation Example

This app uses configuration in code instead of environment variables.

```python
configure_opentelemetry(
    HoneycombOptions(
        debug=True,
        apikey=os.getenv("HONEYCOMB_API_KEY"),
        service_name="otel-python-example"
    )
)
```

This app will send traces to local console with the configured `debug=True`.

To send to Honeycomb, set the API Key:

```bash
HONEYCOMB_API_KEY="your-api-key" poetry run python3 app.py
```

You can configure exporter protocol with this flag:
`OTEL_EXPORTER_OTLP_PROTOCOL=grpc` or `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf`

If you make changes in the package's pyproject.toml you may need to run `poetry build` for the changes to take effect.

If you make changes in python files in src/honeycomb/opentelemetry, with this setup the changes should propagate to this example app upon save.
