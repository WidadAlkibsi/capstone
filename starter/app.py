
import os
from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import unittest
from flask_migrate import Migrate
from models import setup_db, Students, Classes
import logging
from auth import requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy(app)
    # migrate = Migrate(app, db)
    logging.basicConfig(level=logging.DEBUG)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'POST,PATCH,GET,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return render_template('index.html', students=Students.query.all(),
                               classes=Classes.query.all())

    @app.route('/students')
    def get_student():
        students = [student.format() for student in Students.query.all()]
        if not students:
            abort(404)
        return jsonify({'success': True,
                        'students': students})

    @app.route('/classes')
    def get_class():
        classes = [clas.format() for clas in Classes.query.all()]
        if not classes:
            abort(404)
        return jsonify({'success': True,
                        'classes': classes})

    @app.route('/students', methods=['POST'])
    @requires_auth('add:students')
    def post_student(payload):
        try:
            data = request.get_json()
            name = data['student_name']
            classID = data['class_id']
            new_student = Students(student_name=name, class_id=classID)
            new_student.insert()
        except Exception:
            abort(400)
        return jsonify({'success': True,
                        'students': new_student.format()})

    @app.route('/classes', methods=['POST'])
    @requires_auth('add:classes')
    def post_class(payload):
        try:
            data = request.get_json()
            name = data['class_name']
            address = data['address']
            inst = data['instructor']
            new_class = Classes(class_name=name, address=address, instructor=inst)
            new_class.insert()
        except Exception:
             abort(400)
        return jsonify({'success': True,
                    'classes': new_class.format()})

    @app.route('/students/<int:id>', methods=['PATCH'])
    @requires_auth('patch:students')
    def patch_student(payload, id):
        student = Students.query.filter_by(student_id=id).one_or_none()

        if student is None:
            abort(404)
        try:
            data = request.get_json()
            if 'student_name' in data:
                student.student_name = data['student_name']

            if 'class_id' in data:
                student.class_id = data['class_id']

            student.update()

        except Exception:
            abort(400)

        return jsonify({'success': True, 'students': student.format()})

    @app.route('/classes/<int:id>', methods=['DELETE'])
    @requires_auth('delete:classes')
    def delete_class(payload, id):
        clas = Classes.query.filter_by(class_id=id).one_or_none()

        if clas is None:
            # app.logger.error('wdooodies')
            abort(404)

        clas.delete()

        return jsonify({'success': True, 'delete': id})

    # @app.route('/submit', methods=['POST'])
    # def submit():
    #    if request.method =='POST':
    #      student = request.form['student_name']
    #      Class = request.form['Class']
    #      if student == '' or Class== '':
    #        return render_template('index.html', message='Please enter all fields to proceed')
    #      return render_template('success.html')

    @app.route('/login-result')
    def confirm_login():
        return render_template('login-result.html')

# Error Handling

    # @app.errorhandler(AuthError)
    # def authorization_error(AuthError):
    #   return jsonify({
    #     "success": False,
    #     "error": AuthError.status_code,
    #     "message": AuthError.error['description']
    #       }), AuthError.status_code

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(401)
    def wdoodierror(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "wdoodierror"
        }), 401

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False,
                        'error': 400,
                        'message': 'bad request'
                        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({'success': False,
                        'error': 405,
                        'message': 'method not allowed'
                        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'success': False,
                        'error': 500,
                        'message': 'Internal server error'
                        }), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
