FROM python:3.10-alpine AS builder
WORKDIR /src
ADD pyproject.toml poetry.lock /src/

RUN apk add build-base libffi-dev
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-ansi

# ---

FROM python:3.10-alpine
WORKDIR /src

COPY --from=builder /src /src
ADD ./src /src

RUN adduser app -h /src -u 1000 -g 1000 -DH
USER 1000


CMD /app/.venv/bin/python ./main.py
