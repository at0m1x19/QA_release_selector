FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app
ENV RUN_TESTS="false"

ENTRYPOINT ["/bin/sh", "-c", "\
    if [ \"$RUN_TESTS\" = \"true\" ]; then \
        pytest -v; \
    else \
        python3 src/release_scheduler.py \"$@\"; \
    fi", "--"]