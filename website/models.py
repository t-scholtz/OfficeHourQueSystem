from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from os import path
import email

# TODo
# Make databases better - don't really know how this stuff works
# I personally blame Paul
# Maybe make a database which stores all of the names of all fo the class's and reference a que to that class

# Structure 
# There are 5 tables:
#     *One which stores each avaible Course
#     *One which stores the que's active and get forigen key from course
#     *Waitime which store the last 5 people to exit a course que* and calcs WaitTime
#     *Users store access infomation for intructors
#     *Students store students baisc info


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseName = db.Column(db.String(150), unique=True) #aka 115 , 116, 220, 250
    que = db.relationship('Que')
    waitTime = db.relationship('WaitTime')

class Que(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ubit = db.Column(db.String(150), db.ForeignKey('students.ubit'),unique=True)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

class WaitTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ubit = db.Column(db.String(150), db.ForeignKey('students.ubit'))
    time = db.Column(db.DateTime(timezone=True))
    exitTime = db.Column(db.DateTime(timezone=True), default=func.now())
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    ubit = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ubit = db.Column(db.String(150), unique=True)
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    ubid = db.Column(db.String(150))
