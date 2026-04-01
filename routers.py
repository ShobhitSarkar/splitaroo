"""
implementation of the routers connecting to the frontend 
"""
import base64
from typing import Any
from fastapi import FastAPI, File, UploadFile, APIRouter
from llm import get_oai_response
from models import ItemizedReciept, SplitBreakdown

router = APIRouter(prefix="/receipt")

@router.post("/uploadReciept")
async def get_reciept(file: UploadFile = File(...)) -> ItemizedReciept | Any: 
    """
    get an image of the reciept and turn it into an 
    itemized reciept shape 
    
    :param file: reciept 
    :type file: UploadFile
    :return: Reciept data 
    :rtype: ItemizedReciept
    """
    
    file_bytes = await file.read()
    image_encoded = base64.b64encode(file_bytes).decode("utf-8") 
    mime_type = file.content_type
    image_uri = f"data:{mime_type};base64,{image_encoded}"

    itemized_reciept = await get_oai_response("get_itemized_reciept", image_uri)

    return itemized_reciept
    

@router.post("/unstructuredData")
async def who_got_what(unstructured_data: str) -> SplitBreakdown: 
    """
    gets the unstructured data from the user and then maps the people who shared 
    one particular item 
    
    :param unstructered_data: text description of who got what 
    :type str: just purely string description 
    :return: Return the individual split, ie who shared which item 
    :rtype: IndividualSplit
    """

    per_person_split = await get_oai_response("get_shared_item", unstructured_data)

    return per_person_split
