import os 
from typing import Dict 
from dotenv import load_dotenv 
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
oai_api_key = os.getenv("OPENAI_API_KEY")

class ResponseFormat(BaseModel): 
    people: list[str]
    transaction_amounts: dict[int: str]

"""
- identify all the people
- identify which people were involved in which itemized reciept 
- tag the people to the transaction that they were involved in 
"""

client = OpenAI(api_key=oai_api_key) 

response = client.responses.parse(
    model="gpt-5.4-mini",
    input=[
        {"role": "system", "content": "Identify all the people and add it to the people list. "}, 
        {
            "role": "user", 
            "content": "Sam and Alice shared the burger which was 13 dollars, Tom and Hallie shared the pasta which was 20 dollars"
        },
    ], 
    text_format=ResponseFormat
)

print(response.output_parsed)