#: install dependencies
install:
	poetry install

#: install only development dependencies
install_dev:
	poetry install --only dev

#: build a release package
build: install
	poetry build

#: run the unit tests with a clean environment
test: build
	mkdir -p test-results
	unset ${OUR_CONFIG_ENV_VARS} && poetry run pytest tests --junitxml=test-results/junit.xml

#: nitpick lint
lint: install_dev
	poetry run pylint honeycomb tests

#: nitpick style
style: install_dev
	poetry run pycodestyle honeycomb

EXAMPLE_SERVICE_NAME ?= otel-python-example
run_example: export OTEL_SERVICE_NAME := $(EXAMPLE_SERVICE_NAME)
#: fire up an instrumented Python web service; set HONEYCOMB_API_KEY to send data for real
run_example:
	cd examples/hello-world-flask && \
	poetry install && \
	poetry run opentelemetry-instrument flask run

JOB ?= run_tests
#: run a CI job in docker locally, set JOB to override default 'run_tests'
local_ci_exec: forbidden_in_real_ci .circleci/process.yml
	circleci local execute \
	--config .circleci/process.yml \
	--job $(JOB)

.PHONY: install build test lint run_example forbidden_in_real_ci

### Utilities

# ^(a_|b_|c_) :: name starts with any of 'a_', 'b_', or 'c_'
# [^=]        :: [^ ] is inverted set, so any character that isn't '='
# +           :: + is 1-or-more of previous thing
#
# So the match the prefixes, then chars up-to-but-excluding the first '='.
#   example: OTEL_VAR=HEY -> OTEL_VAR
#
# egrep to get the extended regex syntax support.
# --only-matching to output only what matches, not the whole line.
OUR_CONFIG_ENV_VARS := $(shell env | egrep --only-matching "^(HONEYCOMB_|OTEL_)[^=]+")

# To use the circleci CLI to run jobs on your laptop,
# the config must be processed to do things like expand matrix jobs.
.circleci/process.yml: .circleci/config.yml
	circleci config process .circleci/config.yml > .circleci/process.yml

forbidden_in_real_ci:
	@test -z $(CIRCLECI) || \
	( printf "\n🙈 Circle can't local execute in Circle. That'd be 🍌🍌🍌.\n\n" && exit 1 )
