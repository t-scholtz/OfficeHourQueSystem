from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db  
from flask_login import login_required,  current_user
from .models import Que, Course

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    course = Course.query.filter_by(id=2).first()
    waitTime1 = 10
    queSize1 = Que.query.filter_by(course_id=1).count()
    
    return render_template("home.html", user=current_user, waitTime1 = waitTime1, queSize1 = queSize1)


