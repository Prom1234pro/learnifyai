import os
from flask import Blueprint, request, jsonify, send_file, current_app as app

from main.gpt.gpt import generate_content
from main.gpt.tts import run_text_to_speech
from werkzeug.utils import secure_filename

gpt_bp = Blueprint('gpt', __name__)

@gpt_bp.route('/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Question is required'}), 400

    try:
        result = generate_content(question)
    except Exception as e:
        return jsonify({'error': f'Error generating content: {str(e)}'}), 500

    try:
        text = result
        if not text:
            raise KeyError("Text could not be extracted from the response")
    except KeyError as e:
        return jsonify({'error': f'Error processing result: {str(e)}'}), 500

    # Define the audio output file path
    filename = secure_filename("one.mp3")
    output_file = os.path.join('main/static/media', filename)

    try:
        run_text_to_speech(text, output_file)
    except Exception as e:
        return jsonify({'error': f'Text-to-Speech Error: {str(e)}'}), 500

    if not os.path.exists(output_file):
        return jsonify({'error': 'Audio file could not be created'}), 500

    return jsonify({'message': 'Audio generated successfully', 'file_path': filename}), 200


@gpt_bp.route('/get-audio/<filename>', methods=['GET'])
def get_audio(filename):
    try:
        path = f'../main/static/media/{filename}'
        return send_file(path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Error sending audio file: {str(e)}'}), 500