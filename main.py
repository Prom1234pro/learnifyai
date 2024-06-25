from datetime import datetime
from flask import Flask, request, jsonify
from utils import *
import os

app = Flask(__name__)

# Endpoints for uploading an image and converting it to text
@app.route('/imagetotext', methods=['POST'])
def image_to_texd_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    allowed_extensions = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
    file_extension = os.path.splitext(file.filename)[1].lower()[1:]
    if file_extension not in allowed_extensions:
        return jsonify({'error': 'Invalid file extension'}), 400

    # Check MIME type
    try:
        img = Image.open(file)
        if img.format.lower() not in allowed_extensions:
            return jsonify({'error': 'Invalid image format'}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid image file'}), 400

    file.seek(0)
    img = read_files(file)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = timestamp+"_"+os.path.splitext(file.filename)[0]+".txt"
    text = image_to_text(img, filename)
    return jsonify({'text': text})

@app.route('/pdftotext', methods=['POST'])
def pdf_to_text_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    allowed_extensions = {'pdf'}
    file_extension = os.path.splitext(file.filename)[1].lower()[1:]
    if file_extension not in allowed_extensions:
        return jsonify({'error': 'Invalid file extension'}), 400

    pdf_bytes = file.read()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = timestamp+"_"+os.path.splitext(file.filename)[0]+".txt"
    text = pdf_to_text(pdf_bytes, filename)
    return jsonify({'text': text})

@app.route('/scannedpdftotext', methods=['POST'])
def scanned_pdf_to_text_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        # data = request.get_json
        start_page = int(request.form.get('start_page', 1))
        end_page = int(request.form.get('end_page', -1))
    except ValueError:
        return jsonify({'error': 'Invalid start or end page number'})
    
    pdf_bytes = file.read()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = timestamp+"_"+os.path.splitext(file.filename)[0]+".txt"
    text = scanned_pdf_to_text(pdf_bytes, filename, start_page, end_page)
    return jsonify({'text': text})

@app.route('/handwrittenimagetotext', methods=['POST'])
def handwritten_image_to_text_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    image = Image.open(file)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = timestamp+"_"+os.path.splitext(file.filename)[0]+".txt"
    text = handwritten_image_to_text(image, filename)
    print(text)
    return jsonify({'text': text})

# @app.route('/handwrittenimagetotext', methods=['POST'])
# def handwritten_image_to_text():
#     pass 

if __name__ == '__main__':
    app.run(debug=True, port=3000)
