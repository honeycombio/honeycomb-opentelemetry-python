# Examples

## [Hello World Flask](hello-world-flask/)

This example configures the distro using the `opentelemetry_instrument` command, and contains examples of:

- configuring the distro with environment variables
- sending metrics with OpenTelemetry using a counter
- using baggage with context tokens
- manually passing baggage with context
- setting a span attribute

Check out the [Hello-World-Flask Readme](hello-world-flask/README.md) for setting this up!

## [Hello World Python](hello-world/)

This example configures the distro using the `configure_opentelemetry()` function, and contains examples of:

- configuring the distro with a combination of in-code parameters and environment variables
- sending metrics with OpenTelemetry using a counter
- using baggage with context tokens
- setting a span attribute

Check out the [Hello-World Readme](hello-world/README.md) for setting this up!

## Running Examples with Docker-Compose

If you'd like to use Docker for running these examples, there is a `docker-compose.yml` we use for smoke-tests [that may be helpful.](../smoke-tests/docker-compose.yml)

We have the HONEYCOMB_API_ENDPOINT set to an OpenTelemetry Collector. This can be modified as needed or deleted entirely to use the default Honeycomb API Endpoint.

Because each example uses the same port, either comment out the other apps in the docker-compose file, or specify the app and protocol to run:

```bash
cd smoke-tests && docker-compose up --build app-sdk-grpc
```
