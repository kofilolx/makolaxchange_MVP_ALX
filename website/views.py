# Import necessary modules from Flask
from flask import Blueprint, render_template, request, flash, jsonify
# Import login required and current user functions from Flask-Login
from flask_login import login_required, current_user
# Import the database object
from . import db

# Create a Blueprint named 'views'
views = Blueprint('views', __name__)

# Define the route for the index page
@views.route('/')
@login_required  # Require login to access this route
def index():
    # Render the index.html template and pass the current user
    return render_template("index.html", user=current_user)

# Define the route for the terms page
@views.route('/terms')
def terms():
    # Render the terms.html template
    return render_template("terms.html")