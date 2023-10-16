from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail, Message 
from .myemail import send_email,set_mail

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'cse116'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Configure your email server
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = '@gmail.com'
    app.config['MAIL_PASSWORD'] = 'pwd'
    app.config['MAIL_DEFAULT_SENDER'] = '@gmail.com'
    app.config['MAIL_DEBUG'] = True

    db.init_app(app)
    mail = Mail(app) 
    set_mail(mail)

    from .views import views
    from .auth import auth
    from .ques import ques

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(ques, url_prefix='/')

    
    with app.app_context():
        create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .models import  User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    print("here")
    if not path.exists('instance/' + DB_NAME):
        from .models import Course, Que, WaitTime, User, Students
        db.create_all()
        course1 = Course(courseName='115')
        course2 = Course(courseName='116')
        course3 = Course(courseName='220')
        db.session.add(course1)
        db.session.add(course2)
        db.session.add(course3)
        db.session.commit()
        print('Created Database!')
        #TODO - get a list of students UBIT + First name + Last name + ubid
        print("TODO")
        print('Added Students info')

        #FOR TESTING PRUPOSES - DELETE LATER
        student1 = Students(ubit ="bx" , firstName = "bob" , lastName = "x" ,ubid = "1234" )
        student2 = Students(ubit ="by" , firstName = "bobby" , lastName = "y" ,ubid = "2345" )
        student3 = Students(ubit ="bz" , firstName = "bobbiest" , lastName = "z" ,ubid = "3456" )
        db.session.add(student1)
        db.session.add(student2)
        db.session.add(student3)

        que1 = Que(ubit = "bx" , course_id = 1)
        que2 = Que(ubit = "by" , course_id = 1)
        que3 = Que(ubit = "bz" , course_id = 2)
        db.session.add(que1)
        db.session.add(que2)
        db.session.add(que3)
        db.session.commit()
        #TODO - set up email handiling
        send_email('tjscholt@buffalo.edu','testing testing 1 2','TEST - DO NOT REPLY')
        print('sent Test email')
        