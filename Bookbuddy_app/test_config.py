import os
from dotenv import load_dotenv

load_dotenv()

class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bookbuddy.db'  # Use your database URI
    GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False