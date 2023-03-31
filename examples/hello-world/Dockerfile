# to be run with docker-compose in smoke-tests directory
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.3.2

RUN pip install "poetry==$POETRY_VERSION"
# This image is single purpose, so we won't need to compartmentalize Py deps in virtualenvs.
RUN poetry config virtualenvs.create false

COPY README.md pyproject.toml poetry.lock ./
COPY src/ ./src/
RUN poetry install

# Copy the examples into the image and install deps.
COPY examples/ ./examples/
RUN cd ./examples/hello-world && poetry install

# From this point forward, we're operating on the example app.
WORKDIR /app/examples/hello-world
CMD ["python", "app.py"]