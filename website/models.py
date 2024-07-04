from . import db
from flask_login import UserMixin

class Calculator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class units(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    abbreviation = db.Column(db.String(10), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)

class factor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), db.ForeignKey('ingredient.id'), nullable=False)
    conversion_id = db.Column(db.Integer, db.ForeignKey('conversions.id'), nullable=False)

class conversions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_unit = db.Column(db.String(50), db.ForeignKey('units.id'), nullable=False)
    to_unit = db.Column(db.String(50), db.ForeignKey('units.id'), nullable=False)
    factor = db.Column(db.Integer, db.ForeignKey('factor.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    calculator = db.relationship('Calculator')
    # register_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    # last_login = db.Column(db.DateTime, nullable=True)
    # is_admin = db.Column(db.Boolean, default=False)

class access(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class User_access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    access_id = db.Column(db.Integer, db.ForeignKey('access.id'), nullable=False)

