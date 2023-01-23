FROM python:alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.0

RUN pip install "poetry==$POETRY_VERSION"

COPY . .
RUN poetry install
RUN cd ./examples/hello-world && poetry install

CMD ["poetry", "run", "python", "./examples/hello-world/app.py"]