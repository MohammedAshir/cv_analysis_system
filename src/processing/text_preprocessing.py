import re

def preprocess_text(text):
    
    # Replace multiple newlines with a single space
    text = re.sub(r"\n+", "\n", text)

    # Remove unwanted characters (e.g., OCR artifacts)
    text = re.sub(r"[©•]", "", text)

    # Fix broken words split across lines
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)  # Replace single newlines with spaces

    # Standardize section headers (case insensitive)
    text = re.sub(r"(?i)\beducation\b", "Education:", text)
    text = re.sub(r"(?i)\bexperience\b", "Experience:", text)
    text = re.sub(r"(?i)\bskills\b", "Skills:", text)
    text = re.sub(r"(?i)\bprojects\b", "Projects:", text)
    text = re.sub(r"(?i)\bcertifications\b", "Certifications:", text)

    return text.strip()
