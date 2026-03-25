from typing import List
from pydantic import BaseModel

class Item(BaseModel): 
    """
    item of an itemized reciept 
    """
    name: str
    price: float 

class ItemizedReciept(BaseModel): 
    """
    shape of reciept 
    """
    receipt: List[Item]


class SharedItem(BaseModel): 
    """
    each item and the people who shared it 
    """
    item: str 
    people: List[str]

class SplitBreakdown(BaseModel): 
    """
    Record which person got which item 
    """
    items: List[SharedItem]



    


    