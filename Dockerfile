
FROM python:3.13

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

COPY ./pyproject.toml ./uv.lock /app/

RUN uv sync --frozen

COPY ./app /app/app

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "80"]