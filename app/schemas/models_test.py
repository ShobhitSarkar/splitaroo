"""
Tests for app.schemas.models.

Each model is a Pydantic BaseModel with `extra="forbid"`. The flows
to exercise per model are:
  - valid construction
  - missing required field -> ValidationError
  - extra field rejected -> ValidationError
  - wrong type rejected -> ValidationError
"""

import pytest
from pydantic import ValidationError

from app.schemas.models import (
    GuardRailDecision,
    Item,
    ItemizedReciept,
    SharedItem,
    SplitBreakdown,
)


# ---- Item -------------------------------------------------------------------


def test_item_valid_construction() -> None:
    item = Item(name="burger", price=13.0)
    assert item.name == "burger"
    assert item.price == 13.0


def test_item_missing_field_raises() -> None:
    with pytest.raises(ValidationError):
        Item(name="burger")  # type: ignore[call-arg]


def test_item_extra_field_forbidden() -> None:
    with pytest.raises(ValidationError):
        Item(name="burger", price=13.0, extra="nope")  # type: ignore[call-arg]


def test_item_price_must_be_numeric() -> None:
    with pytest.raises(ValidationError):
        Item(name="burger", price="not-a-number")  # type: ignore[arg-type]


# ---- ItemizedReciept --------------------------------------------------------


def test_itemized_reciept_valid_construction() -> None:
    receipt = ItemizedReciept(
        receipt=[Item(name="burger", price=13.0), Item(name="tacos", price=7.0)]
    )
    assert len(receipt.receipt) == 2


def test_itemized_reciept_empty_list_is_valid() -> None:
    receipt = ItemizedReciept(receipt=[])
    assert receipt.receipt == []


def test_itemized_reciept_missing_field_raises() -> None:
    with pytest.raises(ValidationError):
        ItemizedReciept()  # type: ignore[call-arg]


def test_itemized_reciept_rejects_non_item_entries() -> None:
    with pytest.raises(ValidationError):
        ItemizedReciept(receipt=[{"name": "burger"}])  # missing price


# ---- SharedItem -------------------------------------------------------------


def test_shared_item_valid_construction() -> None:
    shared = SharedItem(item="burger", people=["Sam", "Alice"])
    assert shared.item == "burger"
    assert shared.people == ["Sam", "Alice"]


def test_shared_item_empty_people_is_valid() -> None:
    shared = SharedItem(item="burger", people=[])
    assert shared.people == []


def test_shared_item_missing_required_field_raises() -> None:
    with pytest.raises(ValidationError):
        SharedItem(item="burger")  # type: ignore[call-arg]


def test_shared_item_extra_field_forbidden() -> None:
    with pytest.raises(ValidationError):
        SharedItem(item="burger", people=["Sam"], price=1.0)  # type: ignore[call-arg]


# ---- SplitBreakdown ---------------------------------------------------------


def test_split_breakdown_valid_construction() -> None:
    sb = SplitBreakdown(
        items=[SharedItem(item="burger", people=["Sam"])],
    )
    assert sb.items[0].item == "burger"


def test_split_breakdown_missing_field_raises() -> None:
    with pytest.raises(ValidationError):
        SplitBreakdown()  # type: ignore[call-arg]


# ---- GuardRailDecision ------------------------------------------------------


def test_guardrail_decision_valid_true() -> None:
    assert GuardRailDecision(allow=True).allow is True


def test_guardrail_decision_valid_false() -> None:
    assert GuardRailDecision(allow=False).allow is False


def test_guardrail_decision_missing_field_raises() -> None:
    with pytest.raises(ValidationError):
        GuardRailDecision()  # type: ignore[call-arg]


def test_guardrail_decision_extra_field_forbidden() -> None:
    with pytest.raises(ValidationError):
        GuardRailDecision(allow=True, reason="ok")  # type: ignore[call-arg]
