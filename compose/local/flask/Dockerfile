FROM python:3.9-slim-bullseye as builder
WORKDIR /venv
COPY pyproject.toml poetry.lock /venv/

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-ansi

# ---

FROM python:3.9-slim-bullseye
WORKDIR /app

RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y libpq-dev \
    && apt-get install -y telnet netcat \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /venv /venv

COPY ./compose/local/flask/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/flask/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/flask/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

#RUN adduser app -h /app -u 1000 -g 1000 -DH
#USER 1000

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PATH=/venv/.venv/bin:$PATH

# change this to match your application
#CMD /app/.venv/bin/python -m module_name
# or
#ENTRYPOINT ["/start"]
