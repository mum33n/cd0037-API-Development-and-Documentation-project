import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from settings import DB_NAME, DB_PASSWORD, DB_USER
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = 'postgres://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD,
                                                             'localhost:5432', DB_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_invalid_questions(self):
        res = self.client().get('/questions?page=4')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # def test_delete_questions(self):
    #     res = self.client().delete('/questions/10')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_delete_invalid_questions(self):
    #     res = self.client().delete('/questions/100')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)

    def test_search_questions(self):
        term = 'o'
        res = self.client().post('/questions', json={'searchTerm': term})
        data = json.loads(res.data)
        questions = Question.query.filter(
            Question.question.ilike(f'%{term}%')).all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalQuestions'], len(questions))

    def test_add_questions(self):
        res = self.client().post('/questions',
                                 json={'question': '2+2', 'answer': 4, 'category': 1, 'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        categories = Category.query.all()
        length = len(categories)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total'], length)

    def test_get_quizzes(self):
        res = self.client().post(
            '/quizzes', json={'previous_questions': [1], 'quiz_category': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
