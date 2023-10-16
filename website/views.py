from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db  
from flask_login import  current_user
from .models import Que, Course
from .ques import calcWaitTime

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    queSize1 =  Que.query.filter_by(course_id=1).count()
    waitTime1=  calcWaitTime(Course.query.filter_by(id=1).first())

    queSize2 =  Que.query.filter_by(course_id=2).count()
    waitTime2=  calcWaitTime(Course.query.filter_by(id=2).first())

    queSize3 =  Que.query.filter_by(course_id=3).count()
    waitTime3=  calcWaitTime(Course.query.filter_by(id=3).first())
    
    return render_template("home.html", user=current_user, waitTime1 = waitTime1, queSize1 = queSize1, waitTime2 = waitTime2, queSize2 = queSize2, waitTime3 = waitTime3, queSize3 = queSize3)


