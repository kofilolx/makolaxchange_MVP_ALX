# Import the db object from the current package
from . import db
# Import UserMixin for user Model
from flask_login import UserMixin

# Define the User Model with UserMixin
class User(db.Model, UserMixin):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # calculator = db.db.relationship('Calculator')
    # Example commented fields:
    # register_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    # last_login = db.Column(db.DateTime, nullable=True)
    # is_admin = db.Column(db.Boolean, default=False)

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    units = db.relationship('Unit', back_populates='ingredient')
    conversions = db.relationship('Conversion', back_populates='ingredient')

class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    ingredient = db.relationship('Ingredient', back_populates='units')

class Conversion(db.Model):
    __tablename__ = 'conversions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    from_unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    to_unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    conversion_factor = db.Column(db.Float, nullable=False)
    ingredient = db.relationship('Ingredient', back_populates='conversions')
    from_unit = db.relationship('Unit', foreign_keys=[from_unit_id])
    to_unit = db.relationship('Unit', foreign_keys=[to_unit_id])
