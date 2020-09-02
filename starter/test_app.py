import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Students, Classes


class inmotionsTest(unittest.TestCase):
    """This class represents the trivia test case"""
    database_path = os.environ['TESTING_DATABASE_URL']

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)
        jwt = os.environ['JWT_ADMIN']

        self.headers = {"Authorization": "Bearer {}".format(jwt)}
        self.new_class = {"class_name": "any name",
                          "address": "tahlia", "instructor": "anyname"}
        self.new_student = {"student_name": "any name", "class_id": 1}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_student(self):
        student = self.client().get('/students')
        data = json.loads(student.data)

        self.assertEqual(student.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['students'])

    def test_get_class(self):
        clas = self.client().get('/classes')
        data = json.loads(clas.data)

        self.assertEqual(clas.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['classes'])

    def test_delete_class(self):
        clas = self.client().delete('/classes/6', headers=self.headers)
        data = json.loads(clas.data)

        self.assertEqual(clas.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 6)

    def test_405_if_class_does_not_exist(self):
        clas = self.client().delete('/students/1000')
        data = json.loads(clas.data)

        self.assertEqual(clas.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_post_student(self):

        stu = self.client().post('/students', json=self.new_student, headers=self.headers)
        data = json.loads(stu.data)

        self.assertEqual(stu.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_class(self):

        clas = self.client().post('/classes', json=self.new_class, headers=self.headers)
        data = json.loads(clas.data)

        self.assertEqual(clas.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_student(self):
        stu = self.client().patch(
            '/students/1', json={'student_name': 'any name'}, headers=self.headers)
        data = json.loads(stu.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(stu.status_code, 200)

    def test_404_patch_students_notfound(self):
        stu = self.client().patch('/students/10000',
                                  json={'student_name': None}, headers=self.headers)

        data = json.loads(stu.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
