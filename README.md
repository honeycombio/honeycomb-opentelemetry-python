# honeycomb-opentelemetry-python

### Dev Setup
```bash
poetry install
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