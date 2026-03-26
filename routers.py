"""
implementation of the routers connecting to the frontend 
"""
from typing import List, Dict, Annotated
from fastapi import FastAPI, File, UploadFile, APIRouter
from hf import get_hf_client_image
from models import ItemizedReciept, SharedItem
from llm import get_oai_response

router = APIRouter(prefix="/receipt")

@router.post("/uploadReciept")
async def get_reciept(file: UploadFile = File(...)) -> ItemizedReciept | None: 
    """
    get an image of the reciept and turn it into an 
    itemized reciept shape 
    
    :param file: reciept 
    :type file: UploadFile
    :return: Reciept data 
    :rtype: ItemizedReciept
    """
    
    file_bytes = await file.read() 

    print(type(file_bytes))

    itemized_reciept = await get_hf_client_image(file_bytes)

    return itemized_reciept
    

@router.post("/unstructuredData")
async def who_got_what(unstructured_data: str) -> SharedItem: 
    """
    gets the unstructured data from the user and then maps the people who shared 
    one particular item 
    
    :param unstructered_data: text description of who got what 
    :type str: just purely string description 
    :return: Return the individual split, ie who shared which item 
    :rtype: IndividualSplit
    """

    shared_items = await get_oai_response("get_shared_item", unstructured_data) 

    return shared_items
