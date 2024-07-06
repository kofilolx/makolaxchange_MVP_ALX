# Import necessary modules from Flask
from flask import Blueprint, render_template, flash, redirect, url_for, request
# Import User model from models module
from .models import User
# Import db object from current package
from . import db
# Import password hashing functions from Werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
# Import login functions from Flask-Login
from flask_login import login_user, login_required, logout_user, current_user

# Blueprint for user authentication
auth = Blueprint('auth', __name__)

# Route for handling login functionality
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # If request method is POST (form submission)
        email = request.form.get('email')  # Get email from form input
        password = request.form.get('password')  # Get password from form input

        user = User.query.filter_by(email=email).first()  # Query the User table for the user with given email

        if user and check_password_hash(user.password, password): # Check if password matches hashed password
            flash('Logged in successfully!', category='success')  # Flash message for successful login
            login_user(user, remember=True)  # Login the user, with 'remember me' option enabled
            return redirect(url_for('views.index'))  # Redirect to index page after login
        else:
            flash('Incorrect password, try again.', category='error')  # Flash message for incorrect password
    else:
        flash('Email does not exist.', category='error')  # Flash message for non-existing email
        
    # Render the login.html template and pass current_user to template context
return render_template("login.html", user=current_user)


# Decorate the logout function with the route '/logout' under the 'auth' blueprint
@auth.route('/logout')
@login_required  # Require login to access this route
def logout():
    logout_user()  # Logout the current user
    return redirect(url_for('auth.login'))  # Redirect to the login page after logout


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        fullname = request.form.get('fullname')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(fullname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        # elif password1 != password2:
        #     flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, fullname=fullname, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.index'))

    return render_template("register.html")


