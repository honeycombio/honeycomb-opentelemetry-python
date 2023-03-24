#!/usr/bin/env bats

load test_helpers/utilities

CONTAINER_NAME="app-sdk-http-flask"
COLLECTOR_NAME="collector"
OTEL_SERVICE_NAME="otel-python-example"
TRACER_NAME="hello_world_flask_tracer"
METER_NAME="hello_world_flask_meter"

setup_file() {
	docker-compose up --build --detach collector ${CONTAINER_NAME}
	wait_for_ready_app ${CONTAINER_NAME}
	curl --silent localhost:5000
	wait_for_traces
	wait_for_metrics 15
}

teardown_file() {
 	cp collector/data.json collector/data-results/data-${CONTAINER_NAME}.json
	docker-compose stop ${CONTAINER_NAME}
	docker-compose restart collector
	wait_for_flush
}

# TESTS

@test "Auto instrumentation produces a flask span" {
  result=$(span_names_for "opentelemetry.instrumentation.flask")
  assert_equal "$result" '"/"'
}

@test "Manual instrumentation produces parent and child spans with names of spans" {
	result=$(span_names_for ${TRACER_NAME})
	assert_equal "$result" '"child"
"honey"'
}

@test "Manual instrumentation adds custom attribute" {
	result=$(span_attributes_for "${TRACER_NAME}" | jq "select(.key == \"message\").value.stringValue")
	assert_equal "$result" '"hello world!"'
}

@test "BaggageSpanProcessor: key-values added to baggage appear on child spans" {
	result=$(span_attributes_for ${TRACER_NAME} | jq "select(.key == \"honey\").value.stringValue")
	assert_equal "$result" '"bee"'
}

@test "Manual instrumentation produces metrics" {
    result=$(metric_names_for ${METER_NAME})
    assert_equal "$result" '"bee_counter"'
}