from typing import List
from pydantic import BaseModel, ConfigDict

class Item(BaseModel): 
    """
    item of an itemized reciept 
    """
    model_config = ConfigDict(extra="forbid")

    name: str
    price: float 

class ItemizedReciept(BaseModel): 
    """
    shape of reciept 
    """
    model_config = ConfigDict(extra="forbid")
    
    receipt: List[Item]


class SharedItem(BaseModel): 
    """
    each item and the people who shared it 
    """

    model_config = ConfigDict(extra="forbid")

    item: str 
    people: List[str]

class SplitBreakdown(BaseModel): 
    """
    Record which person got which item 
    """

    model_config = ConfigDict(extra="forbid")
    
    items: List[SharedItem]

class GuardRailDecision(BaseModel): 
    """
    Pydantic model to get more reliable decisions
    from the guardrail llm 
    """
    
    allow: bool
