# Dev Setup

Requires [poetry](https://python-poetry.org/docs/) for dependency management and packaging.
Run `poetry --version` to verify it is installed. A minimum of Poetry 1.2 is required.

## Package setup and build

```bash
poetry install
poetry build
```

## Testing

```bash
poetry run pytest tests
```

or

```bash
poetry run coverage run -m pytest tests
```

## Linting & Code Style

```bash
poetry run pylint src
poetry run pycodestyle src tests
```

## Examples

### Example Flask Application

Readme can be found [here](examples/hello-world-flask/README.md) for setting this up.

### Example Python Application

Readme can be found [here](examples/hello-world/README.md) for setting this up.
