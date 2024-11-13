# Import necessary Flask extensions and modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # For database operations
from flask_migrate import Migrate        # For handling database migrations
from flask_login import LoginManager     # For user authentication
from config import Config               # App configuration settings
from extensions import db, login_manager # Shared database and login instances
import os
from dotenv import load_dotenv          # For loading environment variables

def create_app():
    """
    Application Factory Function
    
    This function creates and configures the Flask application. Using a factory function
    is a best practice as it allows for creating multiple instances of the app (useful
    for testing) and keeps the global scope clean.
    """
    # Load environment variables from .env file
    # This allows us to keep sensitive information like API keys separate from the code
    load_dotenv()
    
    # Create the Flask application instance
    # __name__ helps Flask determine the root path of the application
    app = Flask(__name__)
    
    # Load configuration settings
    # This sets up important app settings like secret keys and database URLs
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')  # Used for session security
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///bookbuddy.db')  # Database connection string
    app.config['GOOGLE_BOOKS_API_KEY'] = os.getenv('GOOGLE_BOOKS_API_KEY')  # API key for Google Books
    
    # Initialize Flask extensions
    db.init_app(app)              # Connect SQLAlchemy to Flask app
    migrate = Migrate(app, db)     # Set up database migration capability
    login_manager.init_app(app)    # Initialize login functionality
    
    # Set up database models
    # Using app context to avoid circular imports
    with app.app_context():
        from models import User, Book, ReadingList, UserPreferences
        
        # Create all database tables based on our models
        db.create_all()
    
    # Register blueprints (routes)
    # Blueprints help organize routes into manageable sections
    from routes.books import books_bp
    app.register_blueprint(books_bp, url_prefix='/books')
    
    # Set up user loader for Flask-Login
    # This tells Flask-Login how to find a specific user in the database
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app 