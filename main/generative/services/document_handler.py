from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from PyPDF2 import PdfReader
import google.generativeai as genai
import os

class DocumentService:
    """Handles both regular and scanned PDFs with text extraction and OCR."""

    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-002")

    def extract_page_text(self, reader, page_num):
        """Extract text from a single page of a regular PDF."""
        page = reader.pages[page_num]
        return page.extract_text() or ""

    def pdf_to_text(self, pdf_bytes):
        """Convert a regular PDF to text using parallel processing."""
        reader = PdfReader(BytesIO(pdf_bytes))
        total_pages = len(reader.pages)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(
                executor.map(lambda p: self.extract_page_text(reader, p), range(total_pages))
            )
        return "".join(results)

    def ocr_pdf(self, pdf_file_path):
        """Perform OCR on scanned PDFs using Gemini API."""
        sample_file = genai.upload_file(path=pdf_file_path)
        response = self.model.generate_content(["OCR this image", sample_file])
        return response.text

    def is_scanned_pdf(self, pdf_bytes, num_pages_to_check=5):
        """
        Check if the PDF is a scanned image PDF by attempting to extract text
        from the first few pages.
        """
        reader = PdfReader(BytesIO(pdf_bytes))
        for page_num in range(min(num_pages_to_check, len(reader.pages))):
            text = self.extract_page_text(reader, page_num)
            if text.strip():
                return False  # PDF contains text, not scanned
        return True  # No text found, likely a scanned PDF

    def execute(self, pdf_bytes, file_path=None):
        """
        Execute the appropriate processing method based on the type of PDF.
        If it's scanned, perform OCR; otherwise, extract text directly.
        """
        if self.is_scanned_pdf(pdf_bytes):
            if not file_path:
                raise ValueError("Scanned PDF requires file path for OCR.")
            return self.ocr_pdf(file_path)  # Process with OCR
        else:
            return self.pdf_to_text(pdf_bytes)  # Process with regular extraction
