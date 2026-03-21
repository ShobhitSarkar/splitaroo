from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI() 


@app.post("reciept")

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
