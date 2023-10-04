
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import Que, Course, WaitTime, User
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


ques = Blueprint('ques',__name__)

@ques.route('/cse-115', methods=['GET', 'POST'])
@login_required
def cse115():
    course = Course.query.filter_by(id=1).first()
    
    user_in_queue = check_for_user(course)
    
    waitTime=10
    return render_template("queuePage.html", user=current_user ,course=course, waitTime=waitTime, user_in_queue=user_in_queue)

@ques.route('/cse-116', methods=['GET', 'POST'])
@login_required
def cse116():
    course = Course.query.filter_by(id=2).first()
    
    user_in_queue = check_for_user(course)
    
    waitTime=10
    return render_template("queuePage.html", user=current_user ,course=course, waitTime=waitTime, user_in_queue=user_in_queue)


@ques.route('/cse-220', methods=['GET', 'POST'])
@login_required
def cse220():
    course = Course.query.filter_by(id=3).first()
    
    user_in_queue = check_for_user(course)
    
    waitTime=10
    return render_template("queuePage.html", user=current_user ,course=course, waitTime=waitTime, user_in_queue=user_in_queue)


def check_for_user(course):
    for person in course.que:
        if person.ubit == current_user.ubit:
            return True
    return False


@ques.route('/remove-name', methods=['POST'])
def remove_name():
    data = request.get_json()
    queID = data.get("queID")
    id = Que.query.get(queID)
    if id:
        db.session.delete(id)
        db.session.commit()
    return jsonify({})

@ques.route('/join-que', methods=['POST'])
def join_que():
    data = request.get_json()
    ubit = data.get("ubit")
    courseID = data.get("courseID")
    id = Que.query.filter_by(ubit=ubit).first()
    print(id)
    if id == None:
        new_que_item = Que(ubit = ubit, course_id=courseID)#providing the schema for the note 
        db.session.add(new_que_item) #adding the note to the database 
        db.session.commit()
        flash('Added to queue!', category='success')
    else:
        flash('Already in Que', category='error')

    return jsonify({})

@ques.route('/leave-que', methods=['POST'])
def leave_que():
    print("this was called?")
    data = request.get_json()
    ubit = data.get("ubit")
    courseID = data.get("courseID")
    id = Que.query.filter_by(ubit=ubit).first()
    print(id)
    if  id!=None:
        db.session.delete(id)
        db.session.commit()
        flash('Removed from que', category='success')
    else:
        flash('Not found in que', category='error')

    return jsonify({})


@ques.route('/pop-que', methods=['POST'])
def pop_que():
    print("popping off")
    
    data = request.get_json()
    courseID = data.get("courseID")
    print(courseID)
    # Pop the oldest person from the queue
    oldest_person = Que.query.filter_by(course_id=courseID).order_by(Que.time).first()
    print(oldest_person)
    if oldest_person:
        # Add the person to the WaitTime table
        wait_time_entry = WaitTime(ubit=oldest_person.ubit, course_id=courseID)
        db.session.add(wait_time_entry)
        db.session.commit()

        # Remove the oldest person from the queue
        db.session.delete(oldest_person)
        db.session.commit()

        # Check if there are more than 5 entries in WaitTime and remove the oldest if needed
        wait_time_entries = WaitTime.query.filter_by(course_id=courseID).all()
        if len(wait_time_entries) > 5:
            oldest_wait_time_entry = min(wait_time_entries, key=lambda x: x.time)
            db.session.delete(oldest_wait_time_entry)
            db.session.commit()

    return jsonify({})