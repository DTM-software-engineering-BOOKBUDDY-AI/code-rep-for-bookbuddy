import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = 'your-secret-key-here'  # Change this!
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bookbuddy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Make sure the instance folder exists
    if not os.path.exists('instance'):
        os.makedirs('instance')
    GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
    CACHE_TIMEOUT = 3600  # Cache timeout in seconds