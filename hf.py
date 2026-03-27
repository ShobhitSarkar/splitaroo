import os
import base64
from typing import Any
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from models import ItemizedReciept, SharedItem, Item

load_dotenv()
hf_key = os.getenv('HF_TOKEN')

client = InferenceClient(
    api_key=hf_key,
)

ITEMIZED_RECIEPT_PROMPT = f"""
Your are an expert reciept - analyzer system. You are given the picture of an itemized reciept. Look at the reciept and identify the items bought and their prices. 
After you've gotten the items and prices. Your role is to identify the items and their prices in the picture of 
the reciept. Make sure to only output the items and prices that you see in the picture, it is CRUCIAL that 
you do so. Include the name of the item AND it's price both.
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
    "get_itemized_reciept" : ItemizedReciept,
    "get_shared_item" :  SharedItem 
}

async def get_hf_client_image(image: bytes) -> Any: 
    
    image_bytes = image 

    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/png;base64,{base64_image}"

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "Item",
            "schema": ItemizedReciept.model_json_schema(),
            "strict": True,
        },
    }

    try: 
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-7B-Instruct:hyperbolic",
            response_format=response_format,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": ITEMIZED_RECIEPT_PROMPT
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e: 
        print("An exception occured while calling llm:", e)
    