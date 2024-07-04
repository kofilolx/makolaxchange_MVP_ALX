from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def index():
    return render_template("index.html", user=current_user)

@views.route('/terms')
def terms():
    return render_template("terms.html")
