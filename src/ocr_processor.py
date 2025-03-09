import pytesseract
from PIL import Image
import re
import os

DATA_PATH = "data/"

def extract_text_from_image(image_path):
    """Extract raw text using OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def parse_receipt_data(text):
    """Extract payment details from OCR text."""
    date_pattern = r'\d{2}/\d{2}/\d{4}'
    amount_pattern = r'R\$\s?\d+,\d{2}'
    recipient_pattern = r'Para:\s?(.*)'

    date = re.findall(date_pattern, text)
    amount = re.findall(amount_pattern, text)
    recipient = re.findall(recipient_pattern, text)

    return {
        "date": date[0] if date else "Unknown",
        "amount": amount[0] if amount else "Unknown",
        "recipient": recipient[0] if recipient else "Unknown"
    }

def process_receipts():
    """Process all downloaded receipts."""
    receipts = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".jpg") or file.endswith(".png"):
            text = extract_text_from_image(os.path.join(DATA_PATH, file))
            data = parse_receipt_data(text)
            receipts.append(data)
    
    return receipts

if __name__ == "__main__":
    extracted_data = process_receipts()
    print(extracted_data)