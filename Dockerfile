FROM python:3.10-slim

# Create the working directory
WORKDIR /app

# Install dependencies
ENV PIP_NO_CACHE_DIR=false

RUN pip install -U pip wheel setuptools
RUN pip install poetry==1.1.13

COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes > requirements.txt
RUN pip uninstall poetry -y
RUN pip install -Ur requirements.txt

COPY . .
RUN pip install . --no-deps

ENTRYPOINT ["python3", "src/main.py"]