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

# This project is poetic.
RUN pip install "poetry==$POETRY_VERSION"
# This image is single purpose, so we won't need to compartmentalize Py deps in virtualenvs.
RUN poetry config virtualenvs.create false

# Copy the distro into the image and install deps.
COPY README.md pyproject.toml poetry.lock ./
COPY src/ ./src/
RUN poetry install

# Copy the examples into the image and install deps.
COPY examples/ ./examples/
RUN cd ./examples/hello-world-flask && poetry install

# From this point forward, we're operating on the flask example.
WORKDIR /app/examples/hello-world-flask
CMD ["opentelemetry-instrument", "flask", "run", "--host", "0.0.0.0"]
