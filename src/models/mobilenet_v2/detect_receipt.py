import pytesseract
from PIL import Image
import fitz 

def detect_receipt(file_path):
    """Detecta se o arquivo é um comprovante e tenta extrair os dados."""
    if file_path.endswith(".pdf"):
        return extract_receipt_data_pdf(file_path)
    elif file_path.endswith((".jpg", ".jpeg", ".png")):
        return extract_receipt_data_image(file_path)
    else:
        return False

def extract_receipt_data_pdf(pdf_path):
    """Extrai dados de um PDF usando PyMuPDF e OCR se necessário."""
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    
    if not text.strip():
        image = doc.convert_to_image()
        text = pytesseract.image_to_string(image)
    
    return parse_receipt_text(text)

def extract_receipt_data_image(image_path):
    """Extrai dados de uma imagem usando OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return parse_receipt_text(text)

def parse_receipt_text(text):
    """Extrai valores de quantidade e data do texto extraído."""
    amount = None
    date = None

    for line in text.splitlines():
        if "R$" in line:
            amount = line.strip()
        if "/" in line:
            date = line.strip()

    return {"amount": amount, "date": date}