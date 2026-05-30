"""
root-level conftest.

env vars must be set BEFORE app modules are imported, because
app.core.llm constructs the OpenAI client at module load and reads
OPENAI_BASE_URL/OPENAI_API_KEY at that point.

the ports here pair with the session-scoped httpserver fixtures
in app/conftest.py.
"""

import os

os.environ.setdefault("OPENAI_API_KEY", "test-openai-key")
os.environ.setdefault("OPENAI_BASE_URL", "http://127.0.0.1:8888/v1")

os.environ.setdefault("AWS_ACCESS_KEY_ID", "test-access-key")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "test-secret-key")
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-2")
os.environ.setdefault("AWS_ENDPOINT_URL_SECRETS_MANAGER", "http://127.0.0.1:8889")
