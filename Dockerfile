FROM python:3.13-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

COPY ./pyproject.toml ./uv.lock /app/

RUN uv sync --frozen

COPY ./app /app/app

EXPOSE 80

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "80"]
