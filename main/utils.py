import json
from datetime import timedelta
from flask import session
import numpy as np
import PyPDF2
import cv2
import pytesseract
from PIL import Image
from io import BytesIO
import fitz
import numpy as np

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"



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
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    count = 0
    for page_num in range(len(doc)):
        count += 1
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        for image_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            try:
                image = Image.open(BytesIO(image_bytes))
                gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
                text += pytesseract.image_to_string(gray)
            except Exception as e:
                print(f"Error processing image {image_index} on page {page_num}: {e}")
    print("Count: ", count)
    return text

def read_files(file):
    return np.fromstring(file.read(), np.uint8)

def image_to_text(img):
    image = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
    text = pytesseract.image_to_string(image)

    return text