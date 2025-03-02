from .pdf_processor import extract_text_from_pdf
from .ocr_processor import extract_text_with_ocr

def process_document(file_path):
    text = extract_text_from_pdf(file_path)
    if not text:  # Use OCR if no text is extracted
        print("Switching to OCR...")
        text = extract_text_with_ocr(file_path)
    return text
