from flask import Flask
from extensions import db
from Recommendation import BookRecommender
import requests
import os
from dotenv import load_dotenv
from models import User, UserPreferences

# Load environment variables
load_dotenv()

# Create test Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookbuddy.db'  # Use your database URI
db.init_app(app)

def create_test_user():
    """Create a test user with preferences"""
    with app.app_context():
        # Check if test user exists
        test_user = User.query.filter_by(id=1).first()
        if not test_user:
            test_user = User(
                username="test_user",
                email="test@example.com"
            )
            db.session.add(test_user)
            db.session.commit()

        # Create or update user preferences
        preferences = UserPreferences.query.filter_by(user_id=1).first()
        if not preferences:
            preferences = UserPreferences(
                user_id=1,
                genres="Adventure",
                theme="adventure",
                mood="adventurous",
                length="no_preference",
                maturity="not_mature",
                language="english",
                pace="medium"
            )
            db.session.add(preferences)
        else:
            preferences.genres = "Adventure"
            preferences.theme = "adventure"
            preferences.mood = "adventurous"
            preferences.length = "no_preference"
            preferences.maturity = "not_mature"
            preferences.language = "english"
            preferences.pace = "medium"
        
        db.session.commit()
        return test_user

def get_search_queries_from_preferences(user_prefs):
    """Extract meaningful search terms from user preferences"""
    features = {}
    for pref in user_prefs.split():
        if ':' in pref:
            label, value = pref.split(':', 1)
            if label not in features:
                features[label] = []
            features[label].append(value)
    
    # Build more specific search queries
    queries = []
    
    # Base queries based on genres
    if 'genres' in features:
        genre = features['genres'][0]  # Get the first genre
        queries.append(f"{genre} fiction")
        queries.append(genre)
    
    # Add theme-based queries
    if 'theme' in features:
        theme = features['theme'][0]
        queries.append(f"{theme} fiction")
    
    # Add mood-based queries
    if 'mood' in features:
        mood = features['mood'][0]
        if mood == 'adventurous':
            queries.extend([
                "adventure fiction",
                "action adventure"
            ])
    
    return queries

def fetch_books_from_google_api(query, user_prefs=None, max_results=40):
    """Fetch books from Google Books API with improved filtering"""
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    base_url = "https://www.googleapis.com/books/v1/volumes"
    
    # Build query parameters with explicit English language
    params = {
        'q': f'{query} language:english',  # Add language to query
        'maxResults': max_results,
        'key': api_key,
        'printType': 'books',
        'langRestrict': 'en',  # Explicitly set to English
        'orderBy': 'relevance'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json().get('items', [])
    except Exception as e:
        print(f"Error fetching books: {str(e)}")
        return []

def process_google_books_response(books):
    """Process and clean the Google Books API response"""
    processed_books = []
    for book in books:
        volume_info = book.get('volumeInfo', {})
        
        # Skip books without essential information
        if not all([
            volume_info.get('title'),
            volume_info.get('authors'),
            volume_info.get('description')
        ]):
            continue
        
        # Clean and process the book data
        processed_book = {
            'id': book['id'],
            'title': volume_info['title'],
            'authors': volume_info['authors'],
            'categories': volume_info.get('categories', []),
            'description': volume_info['description'],
            'language': volume_info.get('language', 'unknown'),
            'pageCount': volume_info.get('pageCount', 0),
            'averageRating': volume_info.get('averageRating', 0),
            'maturityRating': volume_info.get('maturityRating', 'NOT_MATURE')
        }
        
        # Additional content-based filtering
        description = processed_book['description'].lower()
        categories = [cat.lower() for cat in processed_book.get('categories', [])]
        
        # Less strict filtering criteria
        has_relevant_content = (
            any(term in description for term in ['adventure', 'action', 'journey', 'quest', 'explore']) or
            any(term in ' '.join(categories) for term in ['adventure', 'action', 'fiction'])
        )
        
        # Exclude non-fiction and educational materials
        is_not_educational = not any(term in description.lower() 
            for term in ['how to', 'textbook', 'study guide', 'manual'])
        
        if has_relevant_content and is_not_educational:
            processed_books.append(processed_book)
    
    return processed_books

def test_recommendation_system():
    with app.app_context():
        # Create test user with preferences
        create_test_user()
        
        # Create recommender instance
        recommender = BookRecommender()
        test_user_id = 1
        
        # Get user preferences
        user_prefs = recommender.get_user_preference_text(test_user_id)
        print("\nUser Preferences:", user_prefs)
        
        # Get search queries
        search_queries = get_search_queries_from_preferences(user_prefs)
        print("\nSearch Queries:", search_queries)
        
        # Fetch and process books
        all_books = []
        for query in search_queries:
            print(f"\nFetching books for query: {query}")
            books = fetch_books_from_google_api(query, user_prefs)
            processed_books = process_google_books_response(books)
            print(f"Found {len(processed_books)} matching books")
            all_books.extend(processed_books)
        
        # Remove duplicates based on book ID
        unique_books = {book['id']: book for book in all_books}.values()
        all_books = list(unique_books)
        
        print(f"\nTotal unique books found: {len(all_books)}")
        
        # Get recommendations
        recommendations = recommender.get_recommendations(
            test_user_id,
            all_books,
            num_recommendations=5
        )
        
        # Print recommendations with debug info
        print("\nTop 5 Book Recommendations:")
        print("-" * 50)
        for i, rec in enumerate(recommendations, 1):
            book = rec['book']
            similarity = rec['similarity']
            
            print(f"\n{i}. {book['title']}")
            print(f"   Authors: {', '.join(book['authors'])}")
            print(f"   Similarity Score: {similarity:.2f}")
            print(f"   Categories: {', '.join(book['categories']) if book['categories'] else 'N/A'}")
            print(f"   Language: {book['language']}")
            print(f"   Rating: {book['averageRating']}/5" if book['averageRating'] else "   Rating: N/A")
            if book['description']:
                print(f"   Description: {book['description'][:150]}...")
            
            recommender.debug_similarity(test_user_id, book)

if __name__ == "__main__":
    test_recommendation_system()