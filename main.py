from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI() 

class SplitNotification(BaseModel): 
    people: Dict[str, int]
    amount_paid: int 
    split_equally: bool | None

class AfterSplit(BaseModel): 
    """
    Returns a dict of the name and amounts owed. 
    """
    amounts: Dict[str, int]
    

@app.get("/split_equally")
def split_equally(split_payload: SplitNotification) -> int:
    """
    :param: payload of shape SplitNotification 
    :return: the amount each person needs to pay 
    
    Main router method that recieves the payload from the frontend 
    """
    print(split_payload)

    amount = split_payload.amount_paid

    number_of_people = len(split_payload.people)

    return amount / number_of_people

@app.get("/split")
def split(split_payload: SplitNotification) -> AfterSplit: 
    """
    Takes in the people, the total amount and how much each 
    person owns
    
    :param split_payload: payload from the frontend about split
    :type split_payload: SplitNotification
    :return: Description
    :rtype: Any
    """

    pass 

    

    
    

def main():
    print("Hello from buddysplit!")


if __name__ == "__main__":
    main()
