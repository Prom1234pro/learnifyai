import requests
import json
import re

# URL of the API endpoint
url = "http://127.0.0.1:5000/admin/create-quiz/obj"

def get_data(data):
    # Use a regular expression to extract the JSON part
    json_text = re.search(r'{.*}', data, re.DOTALL).group(0)
    # Parse the JSON text into a Python dictionary
    json_data = json.loads(json_text)
    return json_data

def create_quiz(res):
    data = get_data(res)
    print(data)
    # Convert the data to JSON format
    json_payload = json.dumps(data)
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json_payload)

    if response.status_code == 201:
        print("Quizzes created successfully!")
    else:
        print(f"Failed to create quizzes. Status code: {response.status_code}, Error: {response.text}")
