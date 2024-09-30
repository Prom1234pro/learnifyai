import json
import os
from flask import Blueprint, request, jsonify, session
from main.authentication.models import User
from main.utils import admin_required, user_required
from main.questions.models import db, PastQuestion

question_bp = Blueprint('past_questions', __name__)

# @question_bp.route('/past-questions', methods=['POST'])
# @admin_required
def create_past_questions(path):
    try:
        with open(path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        return jsonify({'error': 'JSON file not found'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'Error decoding JSON file'}), 400
    
    print(data)
    if isinstance(data, list):
        questions = []
        for item in data:
            question = PastQuestion(
                question=item['question_text'],
                options=item['options'],
                correct_option=item['correct_option'],
                optional_text=item.get('optional_text'),
                year=item['year'],
                school_code=item['school_code'],
                school=item['school'],
                subject=item['subject'],
            )
            questions.append(question)
        db.session.add_all(questions)
        db.session.commit()
        return jsonify({"message": "Questions created successfully!"}), 201
    else:
        return jsonify({"error": "Data must be a list of questions"}), 400

# def create_quiz_obj_(path):
#     try:
#         with open(path, 'r') as json_file:
#             data = json.load(json_file)
#     except FileNotFoundError:
#         return jsonify({'error': 'JSON file not found'}), 404
#     except json.JSONDecodeError:
#         return jsonify({'error': 'Error decoding JSON file'}), 400
    
#     if 'quizzes' not in data or not isinstance(data['quizzes'], list):
#         return jsonify({'error': 'No quizzes data provided or invalid format'}), 400
    
#     course_id = data.get('course_id')
#     year = data.get('year')
    
#     # Validate required fields
#     if not course_id:
#         return jsonify({'error': 'School Code is required'}), 400
    
#     quizzes = data['quizzes']
    
#     for quiz_data in quizzes:
#         try:
#             quiz = QuizQuestion(
#                 topic_name=quiz_data.get('topic_name'),
#                 year=year,
#                 type_=quiz_data.get('type_', 'obj'),
#                 question_text=quiz_data.get('question_text', ''),
#                 answer=quiz_data.get('answer', ''),
#                 hint=quiz_data.get('hint', 'No hint'),
#                 instructions=quiz_data.get('instructions', 'No instructions'),
#                 img=quiz_data.get('img'),
#                 course_id=course_id
#             )
#             db.session.add(quiz)
#             db.session.commit()
            
#             if 'options' in quiz_data and isinstance(quiz_data['options'], list):
#                 options_data = quiz_data['options']
#                 for option_data in options_data:
#                     option = Option(
#                         option_text=option_data['option_text'],
#                         is_correct=option_data['is_correct'],
#                         option_type='quiz_question',
#                         quiz_id=None,
#                         quiz_question_id=quiz.id,
#                     )
#                     db.session.add(option)
#                     if option.is_correct:
#                         quiz.answer = option.option_text
                    
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': f'Error processing quiz: {e}'}), 400
    
#     try:
#         db.session.commit()
#         return jsonify({'message': 'Quizzes created successfully'}), 201
    
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': f'Error committing to database: {e}'}), 500


def read_text(text):
    lines = text.splitlines()
    
    school_code = None
    school = None
    subject = None
    year = None
    correct = None
    optional_text = None
    questions = []
    
    current_question = {}
    current_options = []

    def add_question():
        if "question_text" in current_question and current_options:
            current_question["options"] = current_options.copy()
            current_question["correct_option"] = correct
            questions.append(current_question.copy())
            current_question.clear()
            current_options.clear()

    for line in lines:
        line = line.strip()
        
        if line.startswith("School Code:"):
            school_code = line.split(":", 1)[1].strip()
        
        elif line.startswith("School:"):
            school = line.split(":", 1)[1].strip()
        
        elif line.startswith("Subject:"):
            subject = line.split(":", 1)[1].strip()


        elif line.startswith("Year:"):
            year = line.split(":", 1)[1].strip()
        
        elif line.startswith("Current Instruction:"):
            optional_text = line.split(":", 1)[1].strip()
        
        elif line and not line.startswith(("School Code:", "School:", "Subject:", "Year:", "Current Instruction:")):
            if line.endswith("?"):
                add_question()
                current_question["question_text"] = line
                current_question["optional_text"] = optional_text
                current_question["school_code"] = school_code
                current_question["school"] = school
                current_question["year"] = year
                current_question["subject"] = subject
            else:
                option_parts = line.rsplit(",", 1)
                option_text = option_parts[0].strip()
                is_correct = option_parts[1].strip().lower() == "true" if len(option_parts) > 1 else False
                current_options.append( option_text)
                if is_correct:
                    correct = option_text
    add_question()
    return questions
    

@question_bp.route('/convert-text-to-json2', methods=['POST'])
@admin_required
def convert_text_to_json2():
    if request.method == 'POST':
        data = request.get_json()  # Get JSON data from the request body
        text = data.get('text')    # Extract the text from the data
        print(text)
        # user_id = session.get('user_id')
        # user = User.query.get_or_404(user_id)
        try:
            # is_valid, message = validate_format(text)
            # if not is_valid:
                # return jsonify({'error': message}), 400
            
            json_data = read_text(text)  # Convert text to JSON
            # directory = user.username
            directory = "promise"
            print("here 0")
            json_file_path = os.path.join(directory, 'temp_data.json')
            print("here 1")
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(json_file_path, 'w') as json_file:
                print("here 2")
                json.dump(json_data, json_file, indent=4, separators=(',', ': '))
            print("here 3")
            create_past_questions(json_file_path)
            return jsonify(json_data), 201
        except Exception as e:
            return jsonify({'error': f'Error processing text: {e}'}), 400

    return jsonify({'error': 'Invalid request method'}), 405


@question_bp.route('/past-questions/search', methods=['GET'])
@user_required
def filter_past_questions():
    school_code = request.args.get('school_code')
    subject = request.args.get('subject')
    year = request.args.get('year')

    query = PastQuestion.query
    if school_code:
        query = query.filter_by(school_code=school_code)
    if subject:
        query = query.filter_by(subject=subject)
    if year:
        query = query.filter_by(year=year)

    past_questions = query.all()

    result = [{
        'id': q.id,
        'question': q.question,
        'options': q.options,
        'correct_option': q.correct_option,
        'optional_text': q.optional_text,
        'year': q.year,
        'school_code': q.school_code,
        'school': q.school,
        'subject': q.subject,
        'topic': q.topic,
        'created_at': q.created_at
    } for q in past_questions]
    print(result)
    return jsonify(result), 200


@question_bp.route('/past-questions/<int:id>', methods=['PUT'])
@admin_required
def update_past_question(id):
    data = request.json
    question = PastQuestion.query.get_or_404(id)

    question.question = data.get('question', question.question)
    question.options = data.get('options', question.options)
    question.correct_option = data.get('correct_option', question.correct_option)
    question.optional_text = data.get('optional_text', question.optional_text)
    question.year = data.get('year', question.year)
    question.school_code = data.get('school_code', question.school_code)
    question.school = data.get('school', question.school)
    question.subject = data.get('subject', question.subject)
    question.topic = data.get('topic', question.topic)

    db.session.commit()
    return jsonify({"message": "Question updated successfully!"}), 200

@question_bp.route('/past-questions/submit', methods=['POST'])
@user_required
def submit_multiple_questions():
    data = request.json
    if not isinstance(data, list):
        return jsonify({"error": "Data must be a list of questions with submitted answers"}), 400

    results = []

    for submission in data:
        question_id = submission.get('question_id')
        submitted_option = submission.get('submitted_option')

        # Validate input data
        if not question_id:
            results.append({
                "question_id": question_id,
                "error": "Missing question ID or submitted option"
            })
            continue

        # Fetch the question by its ID
        question = PastQuestion.query.get(question_id)

        if not question:
            results.append({
                "question_id": question_id,
                "error": "Question not found"
            })
            continue

        # Check if the submitted answer matches the correct answer
        is_correct = question.correct_option == submitted_option

        # Append the result for this question
        results.append({
            "question_id": question.id,
            "submitted_option": submitted_option,
            "is_correct": is_correct,
            "correct_option": question.correct_option,
            "feedback": "Correct!" if is_correct else "Incorrect! Try again."
        })

    return jsonify(results), 200

@question_bp.route('/past-questions/<int:id>', methods=['DELETE'])
@admin_required
def delete_past_question(id):
    question = PastQuestion.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted successfully!"}), 200