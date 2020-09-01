import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Students, Classes


class inmotionsTest(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test"
        self.database_path = "postgresql://postgres:widow1998@localhost/test"
        setup_db(self.app, self.database_path)
        jwt=os.environ['JWT_ADMIN']

        self.headers = {"Authorization": "Bearer {}".format(jwt)}
        

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

    # def test_get_class(self):
    #     clas = self.client().get('/classes')
    #     data = json.loads(clas.data)

    #     self.assertEqual(clas.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['classes'])

    # def test_delete_class(self):
    #     clas = self.client().delete('/classes/6', headers=self.headers)
    #     data = json.loads(clas.data)
      

    #     self.assertEqual(clas.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['delete'], 6)

    # def test_405_if_class_does_not_exist(self):
    #     clas = self.client().delete('/students/1000')
    #     data = json.loads(clas.data)

    #     self.assertEqual(clas.status_code, 405)
    #     self.assertEqual(data['success'], False)

    # def test_post_student(self):
    #     # studname = 'kdodp'
    #     # new_student = Students(student_name=studname, class_id = 1)
    #     # new=new_student.format()
    #     stu = self.client().post('/students', json={'student_name': 'any names', 'class_id' : 1}, headers=self.headers)
    #     data = json.loads(stu.data)

    #     self.assertEqual(stu.status_code, 200) 
    #     self.assertEqual(data['success'], True)

    def test_post_class(self):
        classname = "trial class"
        new_class = Classes(class_name='trial class', address='address trial test', instructor='instruhector')
        
        clas = self.client().post('/classes', json=new_class.format(), headers=self.headers)
        data = json.loads(clas.data)

        self.assertEqual(clas.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(data['classes'], True)

    # def test_patch_student(self):
    #     stu = self.client().patch(
    #         '/students/1', json={'student_name': 'any name'}, headers=self.headers)
    #     data = json.loads(stu.data)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(stu.status_code, 200)

    # def test_404_patch_students_notfound(self):
    #     stu = self.client().patch('/students/10000',
    #                               json={'student_name': None}, headers=self.headers)

    #     data = json.loads(stu.data)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['error'], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
