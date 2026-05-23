import pytest 
from httpx import AsyncClient, ASGITransport
from app.schemas.models import ItemizedReciept, Item, SplitBreakdown, SharedItem
from app.core.calculations import split_calculator

_itemized_reciept = ItemizedReciept(
    receipt=[
        Item(name="burger", price=13.00),
        Item(name="tacos", price=7.00),
    ]
)

_split_breakdown = SplitBreakdown(
    items=[
        SharedItem(item="burger", people=["Sam", "Alice"]),
        SharedItem(item="tacos", people=["Sam"]),
    ]
)

"""
xx --------- tests for when input shape is incorrect ---------- xx 
"""
def test_should_raise_if_reciept_is_none() -> None:
    """
    function should raise exception if the itemized reciept is none 
    """

    with pytest.raises(Exception, match="Itemized Reciept is None"): 
        split_calculator(None, _split_breakdown)

def test_should_raise_if_split_is_none() -> None:
    """
    function should raise exception if split breakdown is None 
    """
    
    with pytest.raises(Exception, match="Split Breakdown is None"): 
        split_calculator(_itemized_reciept, None)


def test_should_raise_if_reciept_shape_incorrect() -> None:
    """
    should raise if the shape of itemized reciept is not right 
    """

    _wrong_itemized_reciept = ["sam", "alice"]
    
    with pytest.raises(Exception, match="Itemized Reciept is not the correct shape."): 
        split_calculator(_wrong_itemized_reciept, _split_breakdown)

def test_should_raise_if_breakdown_shape_incorrect() -> None:
    """
    should raise if split breakdown shape is wrong
    """

    _wrong_split_breakdown = ["burger", "13.00"]

    with pytest.raises(Exception, match="The split breakdown is not the correct shape"): 
        split_calculator(_itemized_reciept, _wrong_split_breakdown)


"""
xx ------- happy path --------------- 
"""
def test_calculate_split_happy_path() -> None:
    """
    given the correct reciept and split, it should 
    come up with correct breakdown 
    """
    
    result = split_calculator(_itemized_reciept, _split_breakdown)

    assert result is not None 
    assert result["Sam"] == 13.50 ## sam eats the whole thing soo
    assert result["Alice"] == 6.5 

    



