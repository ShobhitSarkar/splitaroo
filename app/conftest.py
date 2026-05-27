"""
Shared fixtures + fake handlers for tests.

We use pytest-httpserver as a real local HTTP server for external
dependencies (OpenAI, AWS Secrets Manager). No mocking.
"""

import json
from typing import Any

import pytest
from pytest_httpserver import HTTPServer


@pytest.fixture(scope="session")
def httpserver_listen_address():
    # fixed port so app.core.llm's OpenAI client (constructed at
    # module load using OPENAI_BASE_URL) keeps pointing at us.
    return ("127.0.0.1", 8888)


@pytest.fixture(scope="session")
def aws_httpserver():
    server = HTTPServer(host="127.0.0.1", port=8889)
    server.start()
    yield server
    server.clear()
    if server.is_running():
        server.stop()


@pytest.fixture(autouse=True)
def _reset_aws_server(aws_httpserver):
    aws_httpserver.clear()
    yield


def make_openai_response_payload(text_payload: str) -> dict[str, Any]:
    """
    Build a payload mirroring the shape of an OpenAI Responses API
    /v1/responses success body.

    The application reads `response.output[1].content[0].text`, so we
    must produce a payload with a reasoning item at index 0 and a
    message item at index 1 whose first content entry has the given text.
    """
    return {
        "id": "resp_test",
        "object": "response",
        "created_at": 1700000000,
        "status": "completed",
        "model": "gpt-5",
        "output": [
            {
                "type": "reasoning",
                "id": "rs_test",
                "summary": [],
            },
            {
                "type": "message",
                "id": "msg_test",
                "role": "assistant",
                "status": "completed",
                "content": [
                    {
                        "type": "output_text",
                        "text": text_payload,
                        "annotations": [],
                    }
                ],
            },
        ],
        "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2},
        "parallel_tool_calls": False,
        "tool_choice": "auto",
        "tools": [],
        "metadata": {},
    }


def make_transcription_payload(text: str) -> dict[str, Any]:
    return {"text": text}


def expect_openai_responses(httpserver, text_payload: str) -> None:
    """Register a /v1/responses POST that returns the given text for every call."""
    httpserver.expect_request(
        "/v1/responses", method="POST"
    ).respond_with_json(make_openai_response_payload(text_payload))


def queue_openai_responses(httpserver, *text_payloads: str) -> None:
    """
    Register a queue of /v1/responses POSTs. Each incoming call consumes the
    next payload. Use when a route makes multiple OpenAI calls to the same
    URL (e.g. guardrail check + main response). Oneshot handlers do not
    interfere with handlers registered for other URLs.
    """
    for payload in text_payloads:
        httpserver.expect_oneshot_request(
            "/v1/responses", method="POST"
        ).respond_with_json(make_openai_response_payload(payload))


def expect_openai_transcription(httpserver, text: str) -> None:
    httpserver.expect_request(
        "/v1/audio/transcriptions", method="POST"
    ).respond_with_json(make_transcription_payload(text))


def expect_openai_failure(httpserver, status: int = 500) -> None:
    httpserver.expect_request(
        "/v1/responses", method="POST"
    ).respond_with_data("oh no", status=status)


def expect_secretsmanager_get(aws_httpserver, secret_value: str) -> None:
    """SecretsManager GetSecretValue returns a JSON body with SecretString."""
    aws_httpserver.expect_request("/", method="POST").respond_with_json(
        {
            "ARN": "arn:aws:secretsmanager:us-east-2:000000000000:secret:OPENAI_API_KEY",
            "Name": "OPENAI_API_KEY",
            "VersionId": "v1",
            "SecretString": secret_value,
        }
    )


def expect_secretsmanager_failure(aws_httpserver) -> None:
    aws_httpserver.expect_request("/", method="POST").respond_with_json(
        {
            "__type": "ResourceNotFoundException",
            "message": "Secrets Manager can't find the specified secret.",
        },
        status=400,
    )
