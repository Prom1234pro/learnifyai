import json
import re




class QuizService:

    def __init__(self, model):
        self.model = model

        # print(model)
    def execute(self, topic):
        parsed_quiz = None
        try:
            response = self.model.generate_content(topic)
            quiz_data = response.text
            json_pattern = re.compile(r"\{.*\}", re.DOTALL)
            match = json_pattern.search(quiz_data)

            if match:
                json_content = match.group()
                try:
                    # Parse the extracted JSON
                    data = json.loads(json_content)
                    print("Successfully extracted JSON!")
                    # print(json.dumps(data, indent=2))  # Pretty-print the JSON
                    parsed_quiz = json.dumps(data, indent=2)
                    return parsed_quiz
                except json.JSONDecodeError as e:
                    print(f"Invalid JSON format: {e}")
            else:
                return None
            # Attempt to parse the generated JSON response (for validation)
            

        except json.JSONDecodeError:
            return {"error": "Failed to parse the generated JSON response"}
        except Exception as e:
            return {"error": str(e)}