from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI() 

class SplitNotification(BaseModel): 
    people: List[str]
    amount_paid: int 
    split_equally: bool | None


@app.get("/split")
def split(split_payload: SplitNotification): 
    """
    :param: payload of shape SplitNotification 
    :return: the amount each person needs to pay 
    
    Main router method that recieves the payload from the frontend 
    """
    print(split_payload)

    amount = split_payload.amount_paid

    number_of_people = len(split_payload.people)

    return amount / number_of_people
    

def main():
    print("Hello from buddysplit!")


if __name__ == "__main__":
    main()
