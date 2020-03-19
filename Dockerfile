FROM python:3.7.2

ENV PYTHONUNBUFFERED 1

COPY pyproject.toml /

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local && \
    poetry install

COPY . /

WORKDIR /code