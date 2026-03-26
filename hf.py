import os
import base64
from typing import Any
from dotenv import load_dotenv
from huggingface_hub import InferenceClient



load_dotenv()
hf_key = os.getenv('HF_TOKEN')

async def get_hf_client(image: Any) -> Any: 
    
        
    client = InferenceClient(
        api_key=hf_key,
    )

    # Suppose your router gives you raw image bytes
    image_bytes = image  # however you get it

    # Encode to base64 data URI
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/png;base64,{base64_image}"

    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-VL-7B-Instruct:hyperbolic",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Tell me the items in the reciept and how much each costs."
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

    print(completion.choices[0].message)