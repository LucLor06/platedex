from openai import OpenAI
from pydantic import BaseModel
from .models import LicensePlate
from environment_variables import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

class LicensePlateImageValidation(BaseModel):
    is_valid: bool

def license_plate_image_is_valid(license_plate: LicensePlate, ocr_output: str) -> bool:
    SYSTEM_PROMPT = """
    You are a helpful assistant that determines whether a given license plate number appears in OCR output extracted from an image.

    Instructions:
    - Match the plate number **left to right**, in order.
    - Allow **minor substitutions** for visually similar characters (e.g., '1' and 'I', '0' and 'O', 'B' and '8').
    - It's acceptable if there are **one or two extra characters** in the middle of the match, especially around the 3rd or 4th character, which may result from the OCR misreading state seals or icons.
    - Ignore unrelated text like state names, slogans, or decorative words.
    - Return `true` only if the full plate number appears in order (with allowance for the above).
    - Return `false` otherwise.

    You must respond with either `true` or `false` — no explanation or extra output.
    """.strip()
    USER_PROMPT = f"""
    expected plate: {license_plate.number}
    ocr output: {ocr_output}
    """
    response = client.responses.parse(
        model="gpt-4.1-nano-2025-04-14",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": USER_PROMPT,
            },
        ],
        text_format=LicensePlateImageValidation,
    )
    return response.output_parsed.is_valid