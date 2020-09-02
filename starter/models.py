import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
# import json

database_path = 'postgresql://postgres:widow1998@localhost/inmotions' 
db = SQLAlchemy()

def setup_db(app,database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

    


# '''
# Models (Students and Classes )

# '''
class Classes(db.Model): 
   __tablename__ = 'classes'
   class_id = db.Column(db.Integer, primary_key=True)
   class_name = db.Column(db.String(255), nullable=False)
   address = db.Column(db.String(255), nullable=False)
   instructor = db.Column(db.String(255), nullable=False)
   students = db.relationship('Students', backref='classes', lazy=True)

   def __init__(self, class_name, address, instructor):
        self.class_name = class_name
        self.address = address
        self.instructor = instructor 
        
   def insert(self):
        db.session.add(self)
        db.session.commit()

   def update(self):
        db.session.commit()
    
   def delete(self):
        db.session.delete(self)
        db.session.commit() 
   
   def format(self):
        return {
            'id': self.class_id,
            'name': self.class_name,
            'address': self.address,
            'instructor': self.instructor
        }

class Students(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(255), nullable=False)
    class_id = db.Column(db.Integer , db.ForeignKey('classes.class_id') ,nullable=False)

    def __init__(self, student_name, class_id):
        self.student_name = student_name
        self.class_id = class_id
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.student_id,
            'name': self.student_name,
            'class_id': self.class_id
        }
