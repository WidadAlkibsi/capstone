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
        self.database_name = "inmotionstest"
        self.database_path = "postgresql://postgres:widow1998@localhost/inmotionstest"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.headers = {
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRPVW9STVE0dmVaRTE5eGZLclFVVCJ9.eyJpc3MiOiJodHRwczovL2Rldi14b3h3aWRhZC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTU4MDA2MDM0NjY2NzQwMDkxNjEiLCJhdWQiOlsiaW5tb3Rpb25zIiwiaHR0cHM6Ly9kZXYteG94d2lkYWQudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5ODg5MTkzMSwiZXhwIjoxNTk4ODk5MTMxLCJhenAiOiJPQnF5WTdlcXBCQ2ljY1NKcmpRR2VqZVk1MFoyd3NJNiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6Y2xhc3NlcyIsImFkZDpzdHVkZW50cyIsImRlbGV0ZTpjbGFzc2VzIiwicGF0Y2g6c3R1ZGVudHMiXX0.knSujg1ZE1grkkOoe73SK7F7t0jKXB4mwVW1MnBzeJR1txJGAz4hBtwhoo8p7D2kOEq-3dzfpQuUxIjTDnvqRGblS4UT_zQqKO_9b3-V8uY2nkVcKOqRhdts6AzeOUe3bCYiL9nOOM_WKLU2ZDK5NhZIQFkjw8QnUKuQ2va6SE-aMZ0FjVAH4HNDI28SXA3QEbCTPwCAwXT6uc0TOFMZof5vsynirsPEklrlqDkhi452BpMXmhodEfSrdFEf69-i6CUul38uGnxM0fIFu3CRKVLl3dOC5gnsCviIlwG-ObbkqL4NigQeb2uxN8m0w3XFZmCFROAuU5tes5xh272Lvw"
        }

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
        clas = self.client().delete(f'/classes/{1}')
        data = json.loads(clas.data)

        classes = Classes.query.filter_by(Classes.class_id == 1).one_or_none()

        self.assertEqual(clas.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual('delete', 1)

    def test_404_if_class_does_not_exist(self):
        clas = self.client().delete('/students/1000')
        data = json.loads(clas.data)

        self.assertEqual(clas.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_student(self):
        studname = 'Widad'
        new_student = Students(student_name=studname)
        stu = self.client().post('/students', json=self.new_student.format())
        data = json.loads(stu.data)

        self.assertEqual(stu.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_class(self):
        classname = 'trial class'
        new_class = Classes(
            class_name=classname, address="address trial test", instructor="trial instructor test")

        clas = self.client().post('/classes', json=self.new_class.format())
        data = json.loads(clas.data)

        self.assertEqual(clas.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['classes'], True)

    def test_patch_student(self):
        stu = self.client().patch(
            '/students/1', json={'student_name': 'any name'})
        data = json.loads(stu.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(stu.status_code, 200)

    def test_404_patch_students_notfound(self):
        stu = self.client().patch('/students/10000',
                                  json={'student_name': None})

        data = json.loads(stu.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
