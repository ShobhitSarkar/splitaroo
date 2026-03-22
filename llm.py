import os 
from typing import Dict 
from dotenv import load_dotenv 
from openai import OpenAI
from .types import ItemizedReciept, SharedItem

load_dotenv()
oai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=oai_api_key) 

ITEMIZED_RECIEPT_PROMPT = f"""
You are given the picture of the reciept. Your role is to look at the image of the 
reciept and ouput the data in the reciept in the shape of the ItemizedReiept format. 
"""

PER_ITEM_SPLIT_PROMPT = f"""
Your role is to take all of the unstructured data input about which people got 
which item and then turn it into the SharedItem structure. In the SharedItem 
structure, the item is the thing itself and the people list are the people who shared 
that item. 

For example, if get an input like "bob and alice got the burger" the data is going to 
look like \item: "burger", people: ["Sam", "Alex"]
"""

USAGE_SITUATION_FLAGS = {
    1 : "get_itemized_reciept", 
    2 : "get_shared_item",
}

OUTPUT_SHAPES = {
    1: ItemizedReciept, 
    2: SharedItem
}


async def get_oai_response(usage_situation_flag: int,  output_shape: int) -> ItemizedReciept | SharedItem: 
    """
    situation 1: picture of the receipt to the itemized data 
    situation 2: turning unstructured who-got-what into shared item shape 
    
    :param usage_situation_flag: situation_1 or situation_2 
    :type usage_situation_flag: int
    :param output_shape: 1 for ItemizedReciept, 2 for SharedItem
    :type output_shape: int, 1 for ItemizedReciept, 2 for SharedItem 
    :return: Structured Data 
    :rtype: ItemizedReciept | SharedItem 
    """

    if usage_situation_flag not in USAGE_SITUATION_FLAGS: 
        return Exception("Wrong usage situation flag")
    

    if output_shape not in OUTPUT_SHAPES: 
        return Exception("Wrong usage of output shape")
    
    if usage_situation_flag == 1: 
        system_prompt = ITEMIZED_RECIEPT_PROMPT
        output = ItemizedReciept

    if usage_situation_flag == 2:
        system_prompt = PER_ITEM_SPLIT_PROMPT
        output = SharedItem

    response = client.responses.parse(
        model="gpt-4o-2024-08-06",
        input=[
            {"role": "system", "content": {system_prompt}},
            {
                "role": "user",
                "content": "Follow the system prompt only. No deviations.",
            },
        ],
        text_format=output,
    )

    final_result = response.output_parsed

    return final_result