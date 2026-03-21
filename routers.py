from typing import List, Dict
from fastapi import FastAPI, File, UploadFile, APIRouter
from .types import ItemizedReciept

router = APIRouter(prefix="/receipt")

@router.post("/uploadReciept")
def get_reciept(file: UploadFile) -> ItemizedReciept: 
    """
    get an image of the reciept and turn it into an 
    itemized reciept shape 
    
    :param file: reciept 
    :type file: UploadFile
    :return: Reciept data 
    :rtype: ItemizedReciept
    """
    pass 

@router.post("/unstructuredData")
def who_got_what(unstructered_data: str) -> 


