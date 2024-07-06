# Import necessary modules from Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize the SQLAlchemy object
db = SQLAlchemy()
# Define the name of the database file
DB_NAME = "database.db"

# Define the create_app function
def create_app():
    # Create a new Flask app instance
    app = Flask(__name__)
    # Set the secret key for the app
    app.config['SECRET_KEY'] = 'kofilolx'
    # Set the SQLAlchemy database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Initialize the SQLAlchemy object with the app
    db.init_app(app)

    # Import views and authentication blueprints, and models
    from .views import views
    from .auth import auth
    from .models import Calculator, Ingredient, units, factor, conversions, User, User_access, access

    # Create all database tables within the app context
    with app.app_context():
        db.create_all()

    # Register the views blueprint with the app
    app.register_blueprint(views, url_prefix='/')
    # Register the auth blueprint with the app
    app.register_blueprint(auth, url_prefix='/')

    # Initialize the LoginManager
    login_manager = LoginManager()
    # Set the login view for the LoginManager
    login_manager.login_view = 'auth.login'
    # Initialize the LoginManager with the app
    login_manager.init_app(app)

    # Define the user loader callback for the LoginManager
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Return the app instance
    return app

# Define the create_database function
def create_database(app):
    # Check if the database file already exists
    if not path.exists('website/' + DB_NAME):
        # If not, create all database tables within the app context
        with app.app_context():
            db.create_all()
            print("Tables created successfully.")
    else:
        # If it exists, print a message
        print("Database already exists.")

