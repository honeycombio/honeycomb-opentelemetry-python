# Dev Setup

Requires [poetry](https://python-poetry.org/docs/) for dependency management and packaging.
Run `poetry --version` to verify it is installed. A minimum of Poetry 1.2 is required.

Our development workflow leverages the venerable tool Make.
Many of the routine development tasks like running tests or producing a build are automated as make targets.
For an improved Make experience, we recommend, but do not require, [remake](https://remake.readthedocs.io/en/latest/).
`remake --tasks` will output a list of the commonly-used make targets.
`remake` may be substituted for `make` in any of the commands below.

## Package setup and build

```bash
make install
make build
```

## Testing

```bash
make test
```

## Linting & Code Style

```bash
make lint
make style
```

## Examples

### Example Flask Application

Readme can be found [here](examples/hello-world-flask/README.md) for setting this up.

### Example Python Application

Readme can be found [here](examples/hello-world/README.md) for setting this up.

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
