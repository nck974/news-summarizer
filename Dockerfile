FROM python:3.12-slim

RUN apt-get update && apt-get install -y cron && apt-get clean

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false  && \
    poetry install && \
    playwright install-deps && \
    playwright install chromium

COPY . .

RUN chmod +x entrypoint.sh && \
    touch /var/log/cron.log


LABEL version=${VERSION}

ENTRYPOINT ["/app/entrypoint.sh"]