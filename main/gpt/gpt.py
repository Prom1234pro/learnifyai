import os
import requests
import json
import re
from dotenv import load_dotenv

from main.gpt.tts import run_text_to_speech

# Load environment variables from the .env file
load_dotenv()

def generate_content(prompt):
    prompt += '\n Please convert all mathematical symbols into text because this text will be converted to audio files.\n For example\n 2^4 should be converted to 2 raised to power 4'
    # Fetch the API key from the .env file
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        return {'error': 'API key not found. Please check your .env file.'}
    
    # API URL
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'
    
    # Headers and data for the request
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # Check for a successful response
    if response.status_code == 200:
        result = response.json()
        text = result["candidates"][0]["content"]['parts'][0]['text']
        cleaned_text = re.sub(r'[*#]', '', text)
        return cleaned_text  # Return the JSON response from the API
    else:
        return {'error': f'Request failed with status code {response.status_code}', 'details': response.text}

# Usage
if __name__ == '__main__':
    prompt = "What is python"
    result = generate_content(prompt)
    text = result["candidates"][0]["content"]['parts'][0]['text']
    output_file = "output.mp3"  # File where the audio will be saved
    run_text_to_speech(text, output_file)