
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import Que, Course, WaitTime, User, Students
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta
import re

ques = Blueprint('ques',__name__)




@ques.route('/cse-116', methods=['GET', 'POST'])
# @login_required
def cse116():
    courseID = 2
    if request.method == 'POST':
        cardInfo = request.form.get('cardInfo')
        if cardInfo:
            cardNumber = cardInfo[2:18]
            lastName = cardInfo[19:44].rstrip()
            pattern = r'/\^.*\?;'
            match = re.search(pattern, cardInfo)
            card2 = match.group(0)
            personNo = card2[16:22]
            print(personNo)
            student = Students.query.filter_by(ubid=personNo).first()
            ubit = student.ubit
        else:
            ubit = request.form.get('ubit')
        id = Que.query.filter_by(ubit=ubit).first()
        if id == None:
            new_que_item = Que(ubit = ubit, course_id=courseID)
            db.session.add(new_que_item) 
            db.session.commit()
            flash('Added to queue!', category='success')
        else:
            flash('Already in a Que', category='error')
      
        

    course = Course.query.filter_by(id=courseID).first()
    queLength = Que.query.filter_by(course_id=courseID).count()
    waitTime = calcWaitTime(course)

    # Fetch the list of students in the queue with their names
    students_in_queue = db.session.query(Que, Students).join( Students, Que.ubit == Students.ubit).filter(Que.course_id == courseID).all()
    print(course)
    print(students_in_queue)
    return render_template("queuePage.html", user=current_user, course=course, waitTime=waitTime,  queLength=queLength, students_in_queue=students_in_queue)

def check_for_user(course):
    for person in course.que:
        if person.ubit == current_user.ubit:
            return True
    return False

def calcWaitTime(course):
    print("calculating wait time")
    total = timedelta(seconds=0)
    count = WaitTime.query.filter_by(course_id=course.id).count()
    print(count)
    wait_time_entries = WaitTime.query.filter_by(course_id=course.id).all()
    print(wait_time_entries)
    for time in wait_time_entries:
        print(time)
        print(time.time)
        print(time.exitTime)
        total += (time.exitTime - time.time)
    
    if count < 1:
        return 0
    
    # Calculate the average wait time in minutes
    average_wait_time = total.total_seconds() / 60 / count
    return round(average_wait_time, 2)

@ques.route('/remove-name', methods=['POST'])
def remove_name():
    data = request.get_json()
    queID = data.get("queID")
    id = Que.query.get(queID)
    if id:
        db.session.delete(id)
        db.session.commit()
    return jsonify({})

# @ques.route('/join-que', methods=['POST'])
# def join_que():
#     data = request.get_json()
#     ubit = data.get("ubit")
#     courseID = data.get("courseID")
#     id = Que.query.filter_by(ubit=ubit).first()
#     if id == None:
#         new_que_item = Que(ubit = ubit, course_id=courseID)#providing the schema for the note 
#         db.session.add(new_que_item) #adding the note to the database 
#         db.session.commit()
#         flash('Added to queue!', category='success')
#     else:
#         flash('Already in Que', category='error')

#     return jsonify({})

@ques.route('/leave-que', methods=['POST'])
def leave_que():
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
    data = request.get_json()
    courseID = data.get("courseID")
    # Pop the oldest person from the queue
    oldest_person = Que.query.filter_by(course_id=courseID).order_by(Que.time).first()
    print(oldest_person)
    if oldest_person:
        # Remove the oldest person from the queue
        db.session.delete(oldest_person)
        db.session.commit()
        print("popping and stuff")
        wait_time_entry = WaitTime(ubit=oldest_person.ubit,time=oldest_person.time ,course_id=courseID)
        is_in_wait = WaitTime.query.filter_by(ubit = oldest_person.ubit, course_id=courseID).first()
        print(is_in_wait)
        if is_in_wait:
            oldest_wait_time_entry = min(wait_time_entries, key=lambda x: x.time)
            db.session.delete(is_in_wait)
            db.session.commit()
        else:
            wait_time_entries = WaitTime.query.filter_by(course_id=courseID).all()
            if len(wait_time_entries) > 4:
                oldest_wait_time_entry = min(wait_time_entries, key=lambda x: x.time)
                db.session.delete(oldest_wait_time_entry)
                db.session.commit()

        # Add the person to the WaitTime table
        db.session.add(wait_time_entry)
        db.session.commit()
        
        # Check if there are more than 5 entries in WaitTime and remove the oldest if needed
        
    return jsonify({})