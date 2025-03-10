import pytesseract
from PIL import Image

def extract_receipt_data(image_path):
    """Extrai os dados de um comprovante usando OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)

    amount = None
    date = None

    for line in text.splitlines():
        if "R$" in line:
            amount = line.strip()
        if "/" in line:
            date = line.strip()

    return {"amount": amount, "date": date}