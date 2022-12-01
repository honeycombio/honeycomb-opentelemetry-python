# honeycomb-opentelemetry-python

## Dev Setup
Requires [poetry](https://python-poetry.org/docs/) for dependency managament and packaging. 
Run `poetry --version` to verify it is installed.

### Package setup and build
```bash
poetry install
poetry build
```

### Testing
```bash
poetry run pytest tests
```

or 

```bash
poetry run coverage run -m pytest tests
```

### Linting & Code Style
```bash
 poetry run pylint examples src tests
 poetry run pycodestyle examples src tests  
 ```

 ### Example Flask Application
 Readme can be found [here](examples/hello-world-flask/README) for setting this up.