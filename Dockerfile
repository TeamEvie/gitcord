FROM python:3.10-slim

ENV PIP_NO_CACHE_DIR=false
WORKDIR /bot

RUN pip install -U pip wheel setuptools
RUN pip install poetry==1.2.2

COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes > requirements.txt
RUN pip uninstall poetry -y
RUN pip install -Ur requirements.txt

COPY . .

RUN pip install . --no-deps

ENTRYPOINT ["python3", "-m", "gitget"]
