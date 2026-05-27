"""
Tests for app.core.llm.

Cyclomatic complexity / control-flow paths covered:

* get_oai_api_key:
    - successful GetSecretValue response
    - ClientError surfaces as raised exception

* get_oai_response:
    - invalid usage flag -> raises "Wrong usage situation flag"
    - "get_itemized_reciept" success path
    - "get_itemized_reciept" upstream failure wrapped as "Something is going wrong"
    - "get_shared_item" success path
    - "get_shared_item" upstream failure wrapped as "Something went wrong"

* get_stt:
    - returns transcription text from upstream

All upstream HTTP traffic goes to a real local pytest-httpserver
(see app/conftest.py for the session-scoped server bound at the
fixed port the OpenAI client was initialised against).
"""

import asyncio
import json

import pytest

from app.core import llm
from app.core.llm import (
    get_oai_api_key,
    get_oai_response,
    get_stt,
)
from app.schemas.models import ItemizedReciept, SplitBreakdown
from app.conftest import (
    expect_openai_failure,
    expect_openai_responses,
    expect_openai_transcription,
    expect_secretsmanager_failure,
    expect_secretsmanager_get,
)


def _run(coro):
    return asyncio.run(coro)


# ---- get_oai_api_key (boto3 / AWS Secrets Manager) --------------------------


def test_get_oai_api_key_returns_secret_string(aws_httpserver) -> None:
    expect_secretsmanager_get(aws_httpserver, "the-real-secret")

    result = get_oai_api_key()

    assert result == "the-real-secret"


def test_get_oai_api_key_propagates_client_error(aws_httpserver) -> None:
    expect_secretsmanager_failure(aws_httpserver)

    with pytest.raises(Exception):
        get_oai_api_key()


# ---- get_oai_response: invalid flag -----------------------------------------


def test_get_oai_response_rejects_unknown_flag() -> None:
    with pytest.raises(Exception, match="Wrong usage situation flag"):
        _run(get_oai_response("not_a_real_flag", "anything"))


# ---- get_oai_response: itemized receipt flow --------------------------------


def test_get_oai_response_itemized_reciept_happy_path(httpserver) -> None:
    payload = ItemizedReciept(
        receipt=[
            {"name": "burger", "price": 13.0},
            {"name": "tacos", "price": 7.0},
        ]
    ).model_dump_json()
    expect_openai_responses(httpserver, payload)

    result = _run(get_oai_response("get_itemized_reciept", "data:image/png;base64,xx"))

    assert isinstance(result, ItemizedReciept)
    assert {item.name for item in result.receipt} == {"burger", "tacos"}


def test_get_oai_response_itemized_reciept_failure_is_wrapped(httpserver) -> None:
    expect_openai_failure(httpserver, status=500)

    with pytest.raises(Exception, match="Something is going wrong"):
        _run(get_oai_response("get_itemized_reciept", "data:image/png;base64,xx"))


# ---- get_oai_response: shared-item flow -------------------------------------


def test_get_oai_response_shared_item_happy_path(httpserver) -> None:
    payload = SplitBreakdown(
        items=[
            {"item": "burger", "people": ["Sam", "Alice"]},
            {"item": "tacos", "people": ["Sam"]},
        ]
    ).model_dump_json()
    expect_openai_responses(httpserver, payload)

    result = _run(get_oai_response("get_shared_item", "sam and alice had a burger"))

    assert isinstance(result, SplitBreakdown)
    assert result.items[0].item == "burger"
    assert result.items[0].people == ["Sam", "Alice"]


def test_get_oai_response_shared_item_failure_is_wrapped(httpserver) -> None:
    expect_openai_failure(httpserver, status=500)

    with pytest.raises(Exception, match="Something went wrong"):
        _run(get_oai_response("get_shared_item", "anything"))


# ---- get_stt ----------------------------------------------------------------


def test_get_stt_returns_transcribed_text(httpserver) -> None:
    expect_openai_transcription(httpserver, "sam and alice had a burger")

    result = _run(get_stt(b"\x00\x01\x02", "audio.mp3"))

    assert result == "sam and alice had a burger"


# ---- module constants smoke test --------------------------------------------


def test_usage_situation_flags_map_to_models() -> None:
    """sanity check that the flag table still resolves to the expected pydantic shapes."""
    assert llm.USAGE_SITUATION_FLAGS["get_itemized_reciept"] is ItemizedReciept
    assert llm.USAGE_SITUATION_FLAGS["get_shared_item"] is SplitBreakdown
