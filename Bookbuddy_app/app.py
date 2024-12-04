# Import necessary tools and libraries
from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy  # For database management
from flask_migrate import Migrate        # For updating database structure
from flask_login import LoginManager, current_user, login_user, logout_user, login_required  # For user authentication
from config import Config               # App settings
from extensions import db, login_manager # Database and login handling
from forms import LoginForm, SignupForm, ProfileForm  # Forms for user input
import logging  # For keeping track of what's happening in the app
from routes.books import books_bp  # Book-related routes
import os  # For interacting with the operating system
from dotenv import load_dotenv  # For loading secret settings
from Recommendation import BookRecommender
from Recommendation_test import get_search_queries_from_preferences, fetch_books_from_google_api, process_google_books_response

# Load secret settings from .env file
load_dotenv()

# Set up logging to help us track what's happening in our application
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask application - this is the core of our website
app = Flask(__name__)

# Configure the application with necessary settings
app.config.from_object(Config)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')  # For security
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///bookbuddy.db')  # Database location
app.config['GOOGLE_BOOKS_API_KEY'] = os.getenv('GOOGLE_BOOKS_API_KEY')  # Google Books API access

# Set up our database and login system
db.init_app(app)              # Connect to database
migrate = Migrate(app, db)     # Setup database migrations
login_manager.init_app(app)    # Initialize login functionality

# Import our database models (must be after db initialization)
from models import User, Book, ReadingList, UserPreferences

# Add the books blueprint - this organizes our book-related routes
app.register_blueprint(books_bp, url_prefix='/books')

# Tell Flask-Login how to find a specific user
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User ,int(user_id))

# Define what happens when someone visits the homepage
@app.route('/')
@app.route('/home')
def homepage():
    return render_template("homepage.html")

# Routes for different pages (like chapters in a book)
# Each route handles a different page or action on our website

@app.route('/form')
@login_required
def form():
    return render_template('form page/form.html')

@app.route('/recommendation', methods=['GET', 'POST'])
@login_required
def recommendation():
    if request.method == 'POST':
        try:
            # Save preferences to database
            preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()
            
            # Convert lists to comma-separated strings
            themes = ','.join(request.form.getlist('themes')) if request.form.getlist('themes') else ''
            genres = ','.join(request.form.getlist('genres')) if request.form.getlist('genres') else ''
            languages = ','.join(request.form.getlist('preferred_languages')) if request.form.getlist('preferred_languages') else ''
            
            if preferences:
                preferences.style = request.form.get('series', '')
                preferences.theme = themes
                preferences.mood = request.form.get('mood', '')
                preferences.length = request.form.get('length', '')
                preferences.maturity = request.form.get('maturity_rating', '')
                preferences.genres = genres
                preferences.language = languages
                preferences.pace = request.form.get('pace', '')
            else:
                preferences = UserPreferences(
                    user_id=current_user.id,
                    style=request.form.get('series', ''),
                    theme=themes,
                    mood=request.form.get('mood', ''),
                    length=request.form.get('length', ''),
                    maturity=request.form.get('maturity_rating', ''),
                    genres=genres,
                    language=languages,
                    pace=request.form.get('pace', '')
                )
                db.session.add(preferences)
            
            db.session.commit()

            # Create recommender instance
            recommender = BookRecommender()
            
            # Get user preferences
            user_prefs = recommender.get_user_preference_text(current_user.id)
            
            # Log the full text of user preferences
            logger.debug(f"User Preferences Text for User {current_user.id}: {user_prefs}")
            
            # Get search queries
            search_queries = get_search_queries_from_preferences(user_prefs)
            
            # Log the search queries
            logger.debug(f"Search Queries for User {current_user.id}: {search_queries}")
            
            # Fetch and process books
            all_books = []
            for query in search_queries:
                books = fetch_books_from_google_api(query)
                processed_books = process_google_books_response(books)
                all_books.extend(processed_books)
            
            # Remove duplicates
            unique_books = {book['id']: book for book in all_books}.values()
            all_books = list(unique_books)
            
            # Get recommendations
            recommendations = recommender.get_recommendations(
                current_user.id,
                all_books,
                num_recommendations=5
            )
            
            return render_template(
                "recommendation.html", 
                recommendations=recommendations,
                show_results=True
            )

        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            flash(f'Error generating recommendations: {str(e)}', 'error')
            return redirect(url_for('form'))

    # Handle GET request
    return render_template("recommendation.html", show_results=False)

# Routes for user registration and login
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    
    form = SignupForm()
    logger.debug(f"Form submitted: {request.method}")
    
    if form.validate_on_submit():
        logger.debug("Form validated successfully")
        try:
            # Create new user with additional fields
            user = User(
                username=form.username.data,
                email=form.email.data,
                gender=form.gender.data,
                birthday=form.birthday.data
            )
            user.set_password(form.password.data)
            logger.debug(f"Created user object: {user.username}")
            
            # Create preferences
            preferences = UserPreferences(user=user)
            logger.debug("Created preferences object")
            
            # Add to database
            db.session.add(user)
            db.session.add(preferences)
            logger.debug("Added user and preferences to session")
            
            # Commit changes
            db.session.commit()
            logger.info(f"Successfully created user: {user.username}")
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating user: {str(e)}")
            flash(f'Error creating account: {str(e)}', 'error')
    else:
        if form.errors:
            logger.debug(f"Form validation errors: {form.errors}")
    
    return render_template('signup.html', form=form)

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('homepage'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html', form=form)

# Route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('homepage'))

# Route for user profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    # Handle form submission
    if form.validate_on_submit():
        try:
            current_user.username = form.username.data
            current_user.gender = form.gender.data
            current_user.bio = form.bio.data
            current_user.birthday = form.birthday.data
            current_user.telephone = form.telephone.data
            current_user.language = form.language.data
            current_user.privacy = form.privacy.data
            current_user.friends_list = form.friends_list.data
            current_user.block_list = form.block_list.data
            current_user.hide_list = form.hide_list.data
            
            db.session.commit()
            flash('Profile updated successfully! 🎉', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)} ❌', 'error')
            logger.error(f"Profile update error: {str(e)}")
    
    elif request.method == 'GET':
        # Pre-populate form with current user data
        form.username.data = current_user.username
        form.gender.data = current_user.gender
        form.bio.data = current_user.bio
        form.birthday.data = current_user.birthday
        form.telephone.data = current_user.telephone
        form.language.data = current_user.language
        form.privacy.data = current_user.privacy
        form.friends_list.data = current_user.friends_list
        form.block_list.data = current_user.block_list
        form.hide_list.data = current_user.hide_list

    return render_template('profile.html', form=form, user=current_user)

@app.route('/my_lib')
@login_required
def my_lib():
    # Sample book collections
    library_books = {
        'current_books': [
            {
                'id': 1,
                'title': "The Alchemist",
                'author': "Paulo Coelho",
                'progress': 45,
                'image': "01.jpg"
            },
            {
                'id': 2,
                'title': "Dune",
                'author': "Frank Herbert",
                'progress': 30,
                'image': "02.jpg"
            },
            {
                'id': 3,
                'title': "1984",
                'author': "George Orwell",
                'progress': 75,
                'image': "03.jpg"
            }
        ],
        'want_to_read': [
            {
                'id': 4,
                'title': "The Midnight Library",
                'author': "Matt Haig",
                'image': "04.jpg"
            },
            {
                'id': 5,
                'title': "Project Hail Mary",
                'author': "Andy Weir",
                'image': "05.jpg"
            },
            {
                'id': 6,
                'title': "The Seven Husbands of Evelyn Hugo",
                'author': "Taylor Jenkins Reid",
                'image': "06.jpg"
            }
        ],
        'finished_books': [
            {
                'id': 7,
                'title': "The Thursday Murder Club",
                'author': "Richard Osman",
                'image': "07.jpg"
            },
            {
                'id': 8,
                'title': "Klara and the Sun",
                'author': "Kazuo Ishiguro",
                'image': "08.jpg"
            },
            {
                'id': 9,
                'title': "The Invisible Life of Addie LaRue",
                'author': "V.E. Schwab",
                'image': "09.jpg"
            }
        ]
    }
    return render_template('my_lib.html', books=library_books)

# Route for checking users
@app.route('/check_users')
def check_users():
    if app.debug:  # Only allow in debug mode
        users = User.query.all()
        return render_template('check_users.html', users=users)
    return "Not available in production", 403

@app.route('/test_db')
def test_db():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        return 'Database connection successful!'
    except Exception as e:
        return f'Database error: {str(e)}'

@app.route('/search_user', methods=['GET'])
def search_user():
    username = request.args.get('username', '')
    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            # Return only non-sensitive information
            return {
                'found': True,
                'username': user.username,
                'bio': user.bio,
                'profile_picture': user.profile_picture
            }
    return {'found': False}

@app.route('/profile/<username>')
def view_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    # Don't show private profiles unless it's the current user
    if user.privacy == 'private' and (not current_user.is_authenticated or current_user.id != user.id):
        flash('This profile is private.', 'error')
        return redirect(url_for('homepage'))
    return render_template('view_profile.html', profile_user=user)

@app.route('/book_search')
def book_search():
    return render_template('search_results.html')

@app.route('/add-to-reading-list', methods=['POST'])
@login_required
def add_to_reading_list():
    try:
        data = request.get_json()
        book_id = data.get('book_id')
        
        # Check if book already exists in user's reading list
        existing_book = ReadingList.query.filter_by(
            user_id=current_user.id,
            book_id=book_id
        ).first()
        
        if existing_book:
            return jsonify({
                'success': False,
                'message': 'Book is already in your reading list'
            })
        
        # Add book to reading list
        reading_list_item = ReadingList(
            user_id=current_user.id,
            book_id=book_id
        )
        db.session.add(reading_list_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Book added to reading list successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)