from crypt import methods
import math
import os
from unicodedata import category
from click import Abort

from sqlalchemy import true
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(request, selection, number):
    current_page = request.args.get('page', 1, type=int)
    start = (current_page - 1) * number
    end = start + number
    return selection[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'POST, PUT, PATCH, DELETE, UPDATE, GET')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def getCategeories():
        data = Category.query.order_by(Category.id).all()
        formated = [category.format() for category in data]
        result = {}
        for i in formated:
            result[i['id']] = i['type']
        return jsonify({
            'success': True,
            'categories': result,
            'total': len(formated)
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def getQuestions():
        data = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        formarted_categories = [category.format() for category in categories]
        formated = [question.format() for question in data]
        result_categories = {}
        for i in formarted_categories:
            result_categories[i['id']] = i['type']
        paginated = paginate(request, formated, QUESTIONS_PER_PAGE)
        length = len(paginated)
        if length == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'questions': paginated,
                'total_questions': len(formated),
                'categories': result_categories,
                'current_category': '',
                'pages': math.ceil(len(formated)/QUESTIONS_PER_PAGE)
            })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def deleteQuestion(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        if question is None:
            abort(404)
        else:
            question.delete()
            return jsonify({
                "success": True
            })
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def addQuestion():
        data = request.get_json()
        search_term = data.get('searchTerm', None)
        question = data.get('question', None)
        answer = data.get('answer', None)
        difficulty = data.get('difficulty', None)
        category = data.get('category', None)
        try:
            if search_term:
                data = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')).all()
                formated = [question.format() for question in data]
                return jsonify({
                    'success': True,
                    'questions': formated,
                    'totalQuestions': len(formated),
                    'currentCategory': 'Entertainment'
                })
            elif question and answer and difficulty and category:
                newQuestion = Question(
                    question=question, answer=answer, difficulty=difficulty, category=category)
                newQuestion.insert()
                return jsonify({'success': True})
            else:
                abort(422)
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def getQuestion(category_id):
        questions = Question.query.filter(
            Question.category == category_id).all()
        formated = [item.format() for item in questions]
        if formated:
            return jsonify({
                'success': True,
                'questions': formated,
                'total_questions': len(formated),
                'current_category': category_id
            })
        else:
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def getQuizzez():
        body = request.get_json()
        try:
            previous_questions = body.get('previous_questions', [])
            new_questions = Question.query.filter(
                (Question.id).notin_(previous_questions)).all()
            length = len(new_questions)
            new_index = random.randint(0, length)
            formated = [item.format() for item in new_questions]
            return jsonify({
                'success': True,
                'question': formated[new_index]
            })
        except:
            abort(404)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Not Processed'
        }), 422

    @app.errorhandler(405)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    return app
