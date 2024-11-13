# This file defines the structure of our database tables using classes
# Think of each class as a template for a specific type of data we want to store

# Import necessary tools
from extensions import db                # Database connection
from flask_login import UserMixin       # Adds login functionality to User class
from datetime import datetime, date     # For handling dates and times
from werkzeug.security import generate_password_hash, check_password_hash  # For password security

# User class - This is like a template for storing user information
# Similar to how a form has different fields, this class defines what information we store about users
class User(db.Model, UserMixin):
    # Every user needs a unique ID number (like a student ID)
    id = db.Column(db.Integer, primary_key=True)
    
    # Login information
    # These fields must be unique (no two users can have the same email/username)
    email = db.Column(db.String(120), unique=True, nullable=False)      # Must have an email
    username = db.Column(db.String(80), unique=True, nullable=False)    # Must have a username
    password_hash = db.Column(db.String(128))                          # Encrypted password
    
    # Basic profile information
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # When the account was created
    profile_picture = db.Column(db.String(200))  # Link to profile picture
    bio = db.Column(db.Text)                     # User's description about themselves
    
    # Additional profile information
    gender = db.Column(db.String(20))
    birthday = db.Column(db.String(20))
    telephone = db.Column(db.String(20))
    language = db.Column(db.String(20))
    privacy = db.Column(db.String(20), default='public')  # Whether profile is public or private
    
    # Social features - stored as text lists
    friends_list = db.Column(db.Text)  # List of friends
    block_list = db.Column(db.Text)    # List of blocked users
    hide_list = db.Column(db.Text)     # List of hidden users
    
    # Connections to other tables
    # This links the user to their preferences and reading lists
    preferences = db.relationship('UserPreferences', backref='user', uselist=False)
    reading_lists = db.relationship('ReadingList', backref='user', lazy='dynamic')
    
    # This helps print user information in a readable way
    def __repr__(self):
        return f'<User {self.username}>'

    # Security methods for handling passwords
    def set_password(self, password):
        # Convert password into encrypted version
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        # Check if entered password matches encrypted version
        return check_password_hash(self.password_hash, password)

# UserPreferences class - Stores user's reading preferences
class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each preference set
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Links to a user
    
    # Reading preferences
    favorite_genres = db.Column(db.String(500))  # List of favorite book types
    preferred_language = db.Column(db.String(50))  # Preferred reading language
    reading_goal = db.Column(db.Integer)  # How many books they want to read per year
    
    # Settings for email notifications
    email_notifications = db.Column(db.Boolean, default=True)  # Whether to send emails
    
    def __repr__(self):
        return f'<UserPreferences for User {self.user_id}>'

# ReadingList class - Keeps track of books users are reading
class ReadingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each entry
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Which user
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)  # Which book
    status = db.Column(db.String(20))  # Reading status (want to read, reading, finished)
    progress = db.Column(db.Integer, default=0)  # How far they've read (in percentage)
    started_at = db.Column(db.DateTime)  # When they started reading
    finished_at = db.Column(db.DateTime)  # When they finished reading
    
    def __repr__(self):
        return f'<ReadingList {self.user_id} - {self.book_id}>'

# Book class - Stores information about books
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each book
    title = db.Column(db.String(200), nullable=False)  # Book title (required)
    author = db.Column(db.String(200), nullable=False)  # Author name (required)
    cover_image = db.Column(db.String(500))  # Link to book cover image
    genre = db.Column(db.String(100))  # Type of book (fiction, mystery, etc.)
    language = db.Column(db.String(50))  # Language the book is in
    publication_year = db.Column(db.Integer)  # When the book was published
    summary = db.Column(db.Text)  # Short description of the book
    
    # Links to ReadingList to track who's reading this book
    readers = db.relationship('ReadingList', backref='book', lazy='dynamic')
    
    def __repr__(self):
        return f'<Book {self.title}>' 