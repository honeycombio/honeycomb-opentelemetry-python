#!/usr/bin/env bats

load test_helpers/utilities

CONTAINER_NAME="app-sdk-grpc"
COLLECTOR_NAME="collector"
OTEL_SERVICE_NAME="otel-python-example"
TRACER_NAME="hello_world_tracer"
METER_NAME="hello_world_meter"

setup_file() {
	echo "# 🚧" >&3
	docker-compose up --build --detach collector
	wait_for_ready_collector ${COLLECTOR_NAME}
	docker-compose up --build --detach ${CONTAINER_NAME}
	wait_for_traces
	wait_for_metrics
}

teardown_file() {
	cp collector/data.json collector/data-results/data-${CONTAINER_NAME}.json
	docker-compose stop ${CONTAINER_NAME}
	docker-compose restart collector
	wait_for_flush
}

# TESTS

@test "Manual instrumentation produces parent and child spans with names of spans" {
	result=$(span_names_for ${TRACER_NAME})
	assert_equal "$result" '"world"
"hello"'
}

@test "Manual instrumentation adds custom attribute" {
	result=$(span_attributes_for "${TRACER_NAME}" | jq "select(.key == \"message\").value.stringValue")
	assert_equal "$result" '"hello world!"'
}

@test "BaggageSpanProcessor: key-values added to baggage appear on child spans" {
	result=$(span_attributes_for ${TRACER_NAME} | jq "select(.key == \"for_the_children\").value.stringValue")
	assert_equal "$result" '"another_important_value"'
}

@test "Manual instrumentation produces metrics" {
    result=$(metric_names_for ${METER_NAME})
    assert_equal "$result" '"sheep"'
}