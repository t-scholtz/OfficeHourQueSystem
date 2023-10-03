
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ubit = request.form.get('ubit')
        password = request.form.get('password')

        user = User.query.filter_by(ubit=ubit).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Ubit not Found', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    return render_template("sign_up.html", user=current_user)


@auth.route('/student-sign-up', methods=['GET', 'POST'])
def student_sign_up():
    if request.method == 'POST':
        ubit = request.form.get('ubit')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        type = "student"

        user = User.query.filter_by(ubit=ubit).first()

        if user:
            flash('Account already exist', category='error')
        elif(password1 != password2):
            flash('Password does not match', category='error')
        else:
            new_user = User(ubit =ubit, password = generate_password_hash(password1, method='sha256'), type = "student")
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    # return render_template("student_sign_up.html", user=current_user)
    return render_template("student_sign_up.html", user=current_user)

@auth.route('/instructor-sign-up', methods=['GET', 'POST'])
def intsructor_sign_up():
    if request.method == 'POST':
        ubit = request.form.get('ubit')
        code = request.form.get('code')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(ubit=ubit).first()

        if user:
            flash('Account already exist', category='error')
        elif(password1 != password2):
            flash('Password does not match', category='error')
        elif(code != 'bossman'):
            flash('Code is incorect', category='error')
        else:
            new_user = User(ubit =ubit, password = generate_password_hash(password1, method='sha256'), type = "instructor")
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("instructor_sign_up.html", user=current_user)