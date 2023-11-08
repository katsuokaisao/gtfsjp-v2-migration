FROM python:3

WORKDIR /app
COPY Pipfile Pipfile.lock ./

RUN pip install pipenv

RUN pipenv sync
