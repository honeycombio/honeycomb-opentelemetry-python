# hello-world

This simple Django app returns "Hello World". This app uses the `configure_opentelemetry` method from `honeycomb.opentelemetry` to set up OpenTelemetry to export data to Honeycomb through configuration options set in the app's code. It is also possible to set configuration options through the `opentelemetry_instrument` command (see the instructions for automatic instrumenetation [here](https://docs.honeycomb.io/getting-data-in/opentelemetry/python-distro/#automatic-instrumentation)).

## Prerequisites

You'll need [Poetry](https://python-poetry.org/) installed to run the example. Poetry automatically creates a virtual environment to run the example in so you don't need to manage one yourself.

## Running the example

Install application dependencies:

```bash
poetry install
```

Run the application:

```bash
poetry run python manage.py runserver
```

Then navigate to http://127.0.0.1:8000 as shown in the command output and you should see `Hello, world`.

## Distro Instrumentation Example

This app uses configuration configures the OpenTelemetry SDK programmatically in [manage.py](./manage.py).
Alternatively, you can use environment variables as parameters like below:

```python
configure_opentelemetry(
    HoneycombOptions(
        debug=True,
        apikey=os.getenv("HONEYCOMB_API_KEY"),
        service_name="hello-world-django"
    )
)
```

Note: With `debug` set to `True`, spans will also be printed to stdout.

To send to Honeycomb, set your API Key:

```bash
HONEYCOMB_API_KEY="your-api-key" poetry run python manage.py runserver
```

You can configure exporter protocol with this flag:
`OTEL_EXPORTER_OTLP_PROTOCOL=grpc` or `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf`
