from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    ''' Handles login requests and stores login_user in flask session'''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            # Check if typed password is the same as encrypted password stored on database
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)  # Stores user in flask session
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("Email does not exists", category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    ''' Handles sign-up form and add user to database'''
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check input parameters
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category='error')
        # Mudar condições de entrada
        elif len(email) < 4:
            flash("Email must be greater than 4 characters", category='error')
        elif len(firstName) < 2:
            flash("First name must be greater than 1 characters", category='error')
        elif password1 != password2:
            flash("Passwords don't match!", category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 characters", category='error')
        else:
            # Add user to database
            new_user = User(email=email, firstName=firstName,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category='sucess')

            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
