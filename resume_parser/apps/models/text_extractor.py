#resume_parser.apps.models.text_extractor.py
import os
from PIL import Image
import pytesseract
from docx import Document
from pdfminer.high_level import extract_text as extract_text_from_pdf


def extract_text_from_image(file_path):
    img = Image.open(file_path)
    return pytesseract.image_to_string(img)


def extract_text(file_path):
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        doc = Document(file_path)
        return '\n'.join([p.text for p in doc.paragraphs])
    elif ext == ".txt":
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    elif ext in [".jpg", ".jpeg", ".png", ".webp"]:
        return extract_text_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

