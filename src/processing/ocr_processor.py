import pytesseract
from pdf2image import convert_from_path

import pytesseract
from pdf2image import convert_from_path

# Add this line if Tesseract is not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_with_ocr(pdf_path):
    # Convert PDF pages to images
    images = convert_from_path(pdf_path, poppler_path=r'C:\Poppler\Library\bin')

    # Perform OCR on each image
    text = "\n".join([pytesseract.image_to_string(img) for img in images])

    return text

