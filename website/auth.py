
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)
CODEWORD = 'bossman'

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

#TODO - Maybe add minmuin password requirements
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        ubit = request.form.get('ubit')
        code = request.form.get('code')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(ubit=ubit).first()

        if user:
            flash('Slow down cowboy - an account wiht that ubit already exists :(', category='error')
        elif(password1 != password2):
            flash('Passwords don\'t  match', category='error')
        elif(code != CODEWORD):
            flash('Code is incorect', category='error')
        else:
            new_user = User(ubit =ubit, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')

            ##TODO Send confirmation email
            print('Reminder to setup email confimration')

            return redirect(url_for('views.home'))
        
    return render_template("instructor_sign_up.html", user=current_user)