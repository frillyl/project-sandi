from PIL import Image
import pytesseract
import io
from pdf2image import convert_from_bytes
import os

async def perform_ocr(file):
    contents = await file.read()

    if file.filename.endswith('.pdf'):
        images = convert_from_bytes(contents, poppler_path=r"C:\poppler\Library\bin")
        full_text = ""

        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            full_text += f"\n[Halaman {i+1}]\n{text.strip()}\n"

        return {"hasil_ocr": full_text.strip()}

    else:
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image)
        return {"hasil_ocr": text.strip()}
