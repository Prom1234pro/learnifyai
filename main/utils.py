import json
from datetime import timedelta
from flask import session
import numpy as np
import PyPDF2
import cv2
from PIL import Image
from io import BytesIO
import fitz
import numpy as np
import easyocr




SESSION_TIMEOUT = timedelta(hours=24)
ACTIVE_SESSIONS_FILE = 'active_sessions.json'

def load_active_sessions():
    try:
        with open(ACTIVE_SESSIONS_FILE) as file:
            active_sessions_serializable = json.load(file)
            # Convert ISO format strings back to datetime objects
            return {
                user_id: {
                    'email': session_data['email'],
                    'last_activity': session_data['last_activity']
                } for user_id, session_data in active_sessions_serializable.items()
            }
    except FileNotFoundError:
        return {}

# Load active sessions from the JSON file when the application starts

def save_active_sessions(active_sessions):
    with open(ACTIVE_SESSIONS_FILE, 'w') as file:
        json.dump(active_sessions, file)


def is_auth():
    if 'user' in session:
        return True
    else:
        return False
    

def scanned_pdf_to_text(pdf_bytes):
    text = ""
    reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        
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
                
                # Use EasyOCR to extract text from the image
                result = reader.readtext(gray)
                
                # Extract text from the result
                page_text = ' '.join([res[1] for res in result])
                text += page_text + '\n'
            except Exception as e:
                print(f"Error processing image {image_index} on page {page_num}: {e}")
        
        # Optionally, you can remove the break statement if you want to process all pages
        # break
    
    return text


def read_files(file):
    return np.fromstring(file.read(), np.uint8)

def image_to_text(img):
    try:
        # Decode the image if it's in bytes
        image = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_UNCHANGED)
        
        # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'])
        
        # Perform OCR
        result = reader.readtext(image)
        
        # Extract text from the result
        text = ' '.join([res[1] for res in result])
        print("image-to_text was called")
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        return ""