ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
	rm -rf /var/lib/apt/lists/*

WORKDIR /app

#ARG UID=10001
#RUN adduser \
#    --disabled-password \
#    --gecos "" \
#    --home "/nonexistent" \
#    --shell "/sbin/nologin" \
#    --no-create-home \
#    --uid "${UID}" \
#    appuser && \
#    mkdir -p ./tmp
#
#RUN chown appuser:appuser ./tmp
#
#RUN groupadd -g 999 docker && usermod -aG docker appuser

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

#USER appuser

# Copy the source code into the container.
COPY . .

# Run the application.
ENTRYPOINT ["python", "main.py"]
