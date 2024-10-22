class BaseConfig:
    model_name = "gemini-1.5-flash"
    temperature = 1
    top_p = 0.95
    top_k = 64
    max_output_tokens = 8192
    response_mime_type = 'text/plain'
    system_instruction = ""

# Specific Configs for Different Tasks
class AudioConfig(BaseConfig):
    pass

class DocumentConfig(BaseConfig):
    system_instruction = (
        "You are provided with a topic. Your task is to analyze the material and generate questions "
         "strictly based on the topic.\n"
        "1. Generate *at least 5 multiple-choice questions*.\n"
        "2. Each question should have *4 answer options*, with one correct answer clearly marked.\n"
        "3. Format your response as a *JSON object* using the following structure:\n\n"
        "```json\n"
        "{\n"
        "  \"questions\": [\n"
        "    {\n"
        "      \"question\": \"<Your question text here>\",\n"
        "      \"options\": [\n"
        "        \"Option 1\",\n"
        "        \"Option 2\",\n"
        "        \"Option 3\",\n"
        "        \"Option 4\"\n"
        "      ],\n"
        "      \"correct_answer\": \"Correct option here\"\n"
        "    }\n"
        "  ]\n"
        "}\n"
        "```"
    )

class QuizConfig(BaseConfig):
    system_instruction = (
        "You are provided with the following content. Your task is to analyze the material and generate questions "
        "strictly based on the information in the content.\n"
        "1. Extract key information from the content above and generate *at least 5 multiple-choice questions*.\n"
        "2. Each question should have *4 answer options*, with one correct answer clearly marked.\n"
        "3. Format your response as a *JSON object* using the following structure:\n\n"
        "```json\n"
        "{\n"
        "  \"questions\": [\n"
        "    {\n"
        "      \"question\": \"<Your question text here>\",\n"
        "      \"options\": [\n"
        "        \"Option 1\",\n"
        "        \"Option 2\",\n"
        "        \"Option 3\",\n"
        "        \"Option 4\"\n"
        "      ],\n"
        "      \"correct_answer\": \"Correct option here\"\n"
        "    }\n"
        "  ]\n"
        "}\n"
        "```"
    )

class TextConfig(BaseConfig):
    pass