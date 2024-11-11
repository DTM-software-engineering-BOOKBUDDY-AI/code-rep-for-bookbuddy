from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from extensions import db, login_manager
import os
from dotenv import load_dotenv

def create_app():
    # Load environment variables
    load_dotenv()
    
    # Initialize Flask app
    app = Flask(__name__)
    
    # Configure app
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///bookbuddy.db')
    app.config['GOOGLE_BOOKS_API_KEY'] = os.getenv('GOOGLE_BOOKS_API_KEY')
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    
    # Import models (moved inside function to avoid circular imports)
    with app.app_context():
        from models import User, Book, ReadingList, UserPreferences
        
        # Initialize database
        db.create_all()
    
    # Register blueprints
    from routes.books import books_bp
    app.register_blueprint(books_bp, url_prefix='/books')
    
    # Configure login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app 