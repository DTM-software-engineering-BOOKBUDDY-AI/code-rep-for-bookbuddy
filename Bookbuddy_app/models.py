from extensions import db
from flask_login import UserMixin
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    # Primary key - unique identifier for each user
    id = db.Column(db.Integer, primary_key=True)
    
    # Authentication fields
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Profile fields
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_picture = db.Column(db.String(200))  # URL to profile picture
    bio = db.Column(db.Text)
    
    # Add new required fields
    gender = db.Column(db.String(20), nullable=False, default='prefer_not_to_say')
    birthday = db.Column(db.Date, nullable=False, default=date(2000, 1, 1))  # Default date
    
    # Relationships
    preferences = db.relationship('UserPreferences', backref='user', uselist=False)
    reading_lists = db.relationship('ReadingList', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Reading preferences
    favorite_genres = db.Column(db.String(500))  # Store as comma-separated values
    preferred_language = db.Column(db.String(50))
    reading_goal = db.Column(db.Integer)  # Books per year
    
    # Notification preferences
    email_notifications = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<UserPreferences for User {self.user_id}>'

class ReadingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    status = db.Column(db.String(20))  # 'want_to_read', 'reading', 'finished'
    progress = db.Column(db.Integer, default=0)  # Reading progress (%)
    started_at = db.Column(db.DateTime)
    finished_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<ReadingList {self.user_id} - {self.book_id}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    cover_image = db.Column(db.String(500))
    genre = db.Column(db.String(100))
    language = db.Column(db.String(50))
    publication_year = db.Column(db.Integer)
    summary = db.Column(db.Text)
    
    # Relationship with ReadingList
    readers = db.relationship('ReadingList', backref='book', lazy='dynamic')
    
    def __repr__(self):
        return f'<Book {self.title}>' 