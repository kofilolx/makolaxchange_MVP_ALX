# Import the db object from the current package
from . import db
# Import UserMixin for user model
from flask_login import UserMixin

# Define the Calculator model
class Calculator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Define the Ingredient model
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Define the units model
class units(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    abbreviation = db.Column(db.String(10), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)

# Define the factor model
class factor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), db.ForeignKey('ingredient.id'), nullable=False)
    conversion_id = db.Column(db.Integer, db.ForeignKey('conversions.id'), nullable=False)

# Define the conversions model
class conversions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_unit = db.Column(db.String(50), db.ForeignKey('units.id'), nullable=False)
    to_unit = db.Column(db.String(50), db.ForeignKey('units.id'), nullable=False)
    factor = db.Column(db.Integer, db.ForeignKey('factor.id'))

# Define the User model with UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    calculator = db.relationship('Calculator')
    # Example commented fields:
    # register_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    # last_login = db.Column(db.DateTime, nullable=True)
    # is_admin = db.Column(db.Boolean, default=False)

# Define the access model
class access(db.Model):
    id = db.Column(db.Integer, primary_key=True)

# Define the User_access model
class User_access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    access_id = db.Column(db.Integer, db.ForeignKey('access.id'), nullable=False)
