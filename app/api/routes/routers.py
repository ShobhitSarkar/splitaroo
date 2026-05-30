"""
implementation of the routers connecting to the frontend
"""

import base64
from typing import Any
from fastapi import FastAPI, File, UploadFile, APIRouter
from app.core.llm import get_oai_response, get_stt
from app.core.guardrails import guardrail_image, guardrail_text
from app.schemas.models import ItemizedReciept, SplitBreakdown
from app.core.calculations import split_calculator

router = APIRouter(prefix="/receipt")


@router.post("/uploadReciept")
async def get_reciept(file: UploadFile = File(...)) -> ItemizedReciept:
    """
    get an image of the reciept and turn it into an
    itemized reciept shape

    :param file: reciept
    :type file: UploadFile
    :return: Reciept data
    :rtype: ItemizedReciept
    """

    if not isinstance(file, File):
        raise Exception("Given file is not of file object type.")

    if file is None:
        raise Exception("File can't be None.")

    file_bytes = await file.read()
    image_encoded = base64.b64encode(file_bytes).decode("utf-8")
    mime_type = file.content_type
    image_uri = f"data:{mime_type};base64,{image_encoded}"

    guardrail_check = await guardrail_image(image_uri)

    if guardrail_check == False:
        raise Exception("The given input is malicious / inappropriate.")
    else:
        itemized_reciept = await get_oai_response("get_itemized_reciept", image_uri)

    return itemized_reciept


@router.post("/unstructuredData")
async def who_got_what(unstructured_data: str) -> None:
    """
    gets the unstructured data from the user and then maps the people who shared
    one particular item

    :param unstructered_data: text description of who got what
    :type str: just purely string description
    :return: Return the individual split, ie who shared which item
    :rtype: IndividualSplit
    """

    if not isinstance(unstructured_data, str):
        raise Exception("Unstructured data is not string.")

    if unstructured_data is None:
        raise Exception("Unstructured data can't be None.")

    guardrail_check = await guardrail_text(unstructured_data)

    if guardrail_check == False:
        raise Exception("The given input is malicious / inappropriate.")
    else:
        per_person_split = await get_oai_response("get_shared_item", unstructured_data)

    return per_person_split


@router.post("/get_split")
async def get_reciept_details(
    customer_reciept: ItemizedReciept, customer_split_breakdown: SplitBreakdown
) -> dict:
    """
    Router for doing the final calculation

    :param customer_reciept: customer's reciept
    :type customer_reciept: ItemizedReciept
    :param customer_split_breakdown: who got what according to the customer
    :type customer_split_breakdown: SplitBreakdown
    :return: dict where key is the person, value is the amount owed
    :rtype: dict
    """

    if customer_reciept is None:
        raise Exception("customer_reciept can't be None")

    if customer_split_breakdown is None:
        raise Exception("split breakdown can't be none")

    if not isinstance(customer_reciept, ItemizedReciept):
        raise Exception("customer_reciept is not the correct shape")

    if not isinstance(customer_split_breakdown, SplitBreakdown):
        raise Exception("customer_split_breakdown is not in the correct shape")

    final_split = split_calculator(customer_reciept, customer_split_breakdown)

    return final_split


@router.post("/stt")
async def get_voice_breakdown(audio_file: UploadFile = File(...)) -> str:
    """
    Gets the audio from the frontend and returns the transcription.
    This transcription is then going to be used by the who_got_what endpoint
    for the rest of the flow

    :param audio_file: user speech
    :type audio_file: UploadFile (File object)
    :return: transcription
    :rtype: str
    """

    if audio_file.content_type != "audio/mpeg":
        return "Wrong file type supplied."

    file_name = audio_file.filename
    contents = await audio_file.read()

    transcribed_text = await get_stt(contents, file_name)

    guardrail_check = await guardrail_text(transcribed_text)

    if guardrail_check == False:
        raise Exception("Malicious input detected.")

    return transcribed_text
