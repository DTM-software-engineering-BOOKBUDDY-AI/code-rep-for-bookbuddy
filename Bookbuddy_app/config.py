import os

class Config:
    SECRET_KEY = 'your-secret-key-here'  # Change this!
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bookbuddy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Make sure the instance folder exists
    if not os.path.exists('instance'):
        os.makedirs('instance') 