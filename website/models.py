from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# TODo
# Make databases better - don't really know how this stuff works
# I personally blame Paul
# Maybe make a database which stores all of the names of all fo the class's and reference a que to that class

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseName = db.Column(db.String(150), unique=True)
    que = db.relationship('Que')
    waitTime = db.relationship('WaitTime')

class Que(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ubit = db.Column(db.String(150), unique=True)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

class WaitTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ubit = db.Column(db.String(150), unique=True)
    time = db.Column(db.DateTime(timezone=True))
    exitTime = db.Column(db.DateTime(timezone=True), default=func.now())
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    ubit = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    type = db.Column(db.String(150))