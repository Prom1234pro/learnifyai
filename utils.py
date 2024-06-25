from datetime import datetime
import numpy as np
import PyPDF2
import cv2
import pytesseract
from PIL import Image
from io import BytesIO
import fitz
import numpy as np

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract"

def read_files(file):
    return np.fromstring(file.read(), np.uint8)

def image_to_text(img, filename):
    try:
        # Decode the image if it's in bytes
        image = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_UNCHANGED)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(gray)
        
        print("image_to_text was called")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        return ""

def pdf_to_text(pdf_bytes, filename):
    text = ''
    reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
        if page_num > 20:
            break
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    return text

def scanned_pdf_to_text(pdf_bytes, filename, start_page=1, end_page=-1):
    text = ""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    num = 0
    if end_page == -1:
        end_page = len(doc)
    print("starting from page ", start_page, "ending at", end_page)
    for page_num in range(start_page - 1, end_page):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        num += 1
        for image_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            try:
                # Convert image bytes to PIL Image
                image = Image.open(BytesIO(image_bytes))
                
                # Convert PIL Image to numpy array
                image_np = np.array(image)
                
                # Convert to grayscale
                gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
                
                # Use pytesseract to extract text from the image
                page_text = pytesseract.image_to_string(gray)
                text += page_text + '\n'

            except Exception as e:
                print(f"Error processing image {image_index} on page {page_num}: {e}")
        
        # Optionally, you can remove the break statement if you want to process all pages
        break
    with open("documents/"+filename, "w", encoding="utf-8") as f:
        f.write(text)
    return text

def handwritten_image_to_text(image, filename):
    try:
        text = pytesseract.image_to_string(image)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        return None



if __name__ == '__main__':
    # text = handwritten_image_to_text("img\\image_5.jpg")
    # print(text)
    import os
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = timestamp+"_"+os.path.splitext("file.filename")[0]+".txt"
    print(filename)
