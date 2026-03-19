from typing import List
from pydantic import BaseModel

class SplitNotification(BaseModel): 
    people: List[str]
    amount_paid: int 
    split_equally: bool | None

    