from typing import List
from pydantic import BaseModel

class Item(BaseModel): 
    """
    item of an itemized reciept 
    """
    name: str
    price: int 

class ItemizedReciept(BaseModel): 
    """
    shape of reciept 
    """
    receipt: List[Item]


class IndividualSplit(BaseModel): 
    """
    each person and the list
    """
    item: str 
    people: List[str]

class TotalSplit(BaseModel): 
    """
    Record which person got which item 
    """
    items: List[IndividualSplit]


    


    