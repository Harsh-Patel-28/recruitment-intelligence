import fitz  # this is PyMuPDF, weird import name but that's the package
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    
    # Open the PDF directly from bytes in memory (not from a file path)
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    
    doc.close()
    return full_text


if __name__ == "__main__":
    with open("test_resume.pdf", "rb") as f:
        pdf_bytes = f.read()
    
    text = extract_text_from_pdf(pdf_bytes)
    print(text)