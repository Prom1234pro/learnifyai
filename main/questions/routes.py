from flask import Blueprint, request, jsonify
from main.utils import admin_required, user_required
from models import db, PastQuestion

question_bp = Blueprint('past_questions', __name__)

@question_bp.route('/past-questions', methods=['POST'])
@admin_required
def create_past_questions():
    data = request.json
    if isinstance(data, list): 
        questions = []
        for item in data:
            question = PastQuestion(
                question=item['question'],
                options=item['options'],
                correct_option=item['correct_option'],
                optional_text=item.get('optional_text'),
                year=item['year'],
                school_code=item['school_code'],
                school=item['school'],
                subject=item['subject'],
                topic=item.get('topic')
            )
            questions.append(question)
        db.session.add_all(questions)
        db.session.commit()
        return jsonify({"message": "Questions created successfully!"}), 201
    else:
        return jsonify({"error": "Data must be a list of questions"}), 400


@question_bp.route('/past-questions/search', methods=['GET'])
@user_required
def filter_past_questions():
    school = request.args.get('school')
    subject = request.args.get('subject')
    year = request.args.get('year')

    query = PastQuestion.query
    if school:
        query = query.filter_by(school=school)
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


@question_bp.route('/past-questions/<int:id>', methods=['DELETE'])
@admin_required
def delete_past_question(id):
    question = PastQuestion.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted successfully!"}), 200
