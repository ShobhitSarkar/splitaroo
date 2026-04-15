import os 
import boto3 
from botocore.exceptions import ClientError
from typing import Any, Dict 
from dotenv import load_dotenv 
from openai import OpenAI
from app.schemas.models import ItemizedReciept, SplitBreakdown

def get_oai_api_key():

    secret_name = "OPENAI_API_KEY"
    region_name = "us-east-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    oai_api_key = get_secret_value_response['SecretString']

    return oai_api_key


# load_dotenv()


oai_api_key = get_oai_api_key()


client = OpenAI(api_key=oai_api_key) 

ITEMIZED_RECIEPT_PROMPT = f"""
Your are an expert reciept - analyzer system. You are given the picture of an itemized reciept. Look at the reciept and identify the items bought and their prices. 
After you've gotten the items and prices. Your role is to identify the items and their prices in the picture of 
the reciept. Make sure to only output the items and prices that you see in the picture, it is CRUCIAL that 
you do so. Include the name of the item AND it's price both. 
"""

PER_ITEM_SPLIT_PROMPT = f"""
Your role is to take all of the unstructured data input about which people got 
which item and then turn it into the SplitBreakdown structure. In the SplitBreakdown 
structure, the item is the thing itself and the people list are the people who shared 
that item. Make sure to come back with all the items in the given data and who shared what. 

It's crtical that you don't miss out on the items given to you. 

For example, if get an input like "bob and alice got the burger" the data is going to 
look like \item: "burger", people: ["Sam", "Alex"]
"""

USAGE_SITUATION_FLAGS = {
    "get_itemized_reciept" : ItemizedReciept,
    "get_shared_item" :  SplitBreakdown 
}

async def get_oai_response(usage_situation_flag: str, router_content: str) -> ItemizedReciept | SplitBreakdown: 
    """
    situation 1: picture of the receipt to the itemized data 
    situation 2: turning unstructured who-got-what into shared item shape 
    
    :param usage_situation_flag: situation_1 or situation_2 
    :type usage_situation_flag: int
    :param output_shape: 1 for ItemizedReciept, 2 for SplitBreakdown
    :type output_shape: int, 1 for ItemizedReciept, 2 for SplitBreakdown 
    :return: Structured Data 
    :rtype: ItemizedReciept | SplitBreakdown 
    """

    if usage_situation_flag not in USAGE_SITUATION_FLAGS: 
        raise Exception("Wrong usage situation flag")
    
    
    if usage_situation_flag == "get_itemized_reciept": 
        system_prompt = ITEMIZED_RECIEPT_PROMPT
        output_model = USAGE_SITUATION_FLAGS["get_itemized_reciept"]

        try: 
            response = client.responses.parse(
                model="gpt-5",
                reasoning={"effort": "low"},
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "ItemizedReciept",
                        "schema": output_model.model_json_schema()
                    }
                }, 
                input=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_image",
                                "image_url": router_content
                            },
                        ],
                    },
                ]
            )

            response_object = response.output[1].content[0].text

            result = ItemizedReciept.model_validate_json(response_object)
        
        except Exception as e: 
            raise Exception(f"Something is going wrong: {e}")
        
    
    if usage_situation_flag == "get_shared_item":
        system_prompt = PER_ITEM_SPLIT_PROMPT
        output_model = USAGE_SITUATION_FLAGS["get_shared_item"]

        try: 
            response = client.responses.parse(
                model="gpt-5",
                reasoning={"effort": "low"},
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "SplitBreakdown",
                        "schema": output_model.model_json_schema()
                    }
                }, 
                input=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": router_content
                            },
                        ],
                    },
                ]
            )

            response_object = response.output[1].content[0].text

            result = SplitBreakdown.model_validate_json(response_object)
        
        except Exception as e: 
            raise Exception(f"Something went wrong: {e}")
        
    return result 

    


    