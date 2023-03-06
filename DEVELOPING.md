# Dev Setup

Requires [poetry](https://python-poetry.org/docs/) for dependency management and packaging.
Run `poetry --version` to verify it is installed. A minimum of Poetry 1.2 is required.

Our development workflow leverages a `Makefile` to define "targets" for most of the routine development tasks for this project, like running tests or producing a build.
These targets can be run with the venerable build tool [GNU Make](https://www.gnu.org/software/make/) or one of its variants, like [remake](https://remake.readthedocs.io/en/latest/).

While the `make` command is possibly already installed on your computer, we recommend `remake` which extends GNU Make to add profiling, debugging, improved error messages, and usage help text for targets.
`remake --tasks` will output a list of the commonly-used make targets.
`remake` may be substituted for `make` in any of the commands below.

## Package setup and build

```bash
make install
make build
```

## Examples
Check out the [Example Application overview](/examples/). 

Note: Changes to python files in `src/honeycomb/opentelemetry` should propagate to the example applications upon save. Changes in the honeycomb.opentelemetry's pyproject.toml may need a `poetry build` to take effect in the example applications.

### Running with Docker-Compose

In the smoke-tests directory there exists a `docker-compose.yml` to run in Docker.

Because each example uses the same port, either comment out the other apps in the docker-compose file, or specify the app to run:

```bash
cd smoke-tests && docker-compose up --build app-sdk-grpc
```

## Testing

### Unit Tests

```bash
make test
```

### Smoke Tests

Install `bats-core` and `jq` for local testing:

```bash
brew install bats-core
brew install jq
```

```bash
make smoke-sdk
# or specify a single protocol like with http or grpc:
make smoke-sdk-grpc

# To tidy up afer a test run, use:
make unsmoke
```

## Linting & Code Style

```bash
make lint
make style
```

## Troubleshooting

Sometimes cache can cause unexpected behavior.

### Clear pycache and dist

Use `make clean` to clear out all dist directories and caches in `__pycache__`

### Clear poetry cache

To see where the poetry virtual environment exists, use `poetry env info` or `poetry env list --full-path` as referenced in [Poetry docs](https://python-poetry.org/docs/managing-environments/).

For example, here's an interaction that removes a poetry virtual environment that exists for the main project on a user's macbook:

```bash
# list path to virtual environment
➜ poetry env list --full-path
/Users/alice/Library/Caches/pypoetry/virtualenvs/honeycomb-opentelemetry-p9yAYVmc-py3.10 (Activated)
# remove virtual environment
➜ poetry env remove python3.10
Deleted virtualenv: /Users/alice/Library/Caches/pypoetry/virtualenvs/honeycomb-opentelemetry-p9yAYVmc-py3.10
```

Then go through the steps again to install and build, and there will be a new virtual environment.
