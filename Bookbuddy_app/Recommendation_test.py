from flask import Flask
from extensions import db
from Recommendation import BookRecommender
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create test Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookbuddy.db'  # Use your database URI
db.init_app(app)

def fetch_books_from_google_api(query, max_results=40):
    """Fetch books from Google Books API"""
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    base_url = "https://www.googleapis.com/books/v1/volumes"

    params = {
        'q': query,
        'maxResults': max_results,
        'key': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json().get('items', [])
    except Exception as e:
        print(f"Error fetching books: {str(e)}")
        return []

def process_google_books_response(books):
    """Process Google Books API response into our required format"""
    processed_books = []

    for book in books:
        volume_info = book.get('volumeInfo', {})
        processed_book = {
            'id': book.get('id'),
            'title': volume_info.get('title', 'Unknown Title'),
            'authors': volume_info.get('authors', []),
            'categories': volume_info.get('categories', []),
            'description': volume_info.get('description', ''),
            'language': volume_info.get('language', ''),
            'pageCount': volume_info.get('pageCount', 0),
            'publishedDate': volume_info.get('publishedDate', ''),
            'imageLinks': volume_info.get('imageLinks', {}),
            'averageRating': volume_info.get('averageRating', 0)
        }
        processed_books.append(processed_book)

    return processed_books

def test_recommendation_system():
    with app.app_context():
        # Create recommender instance
        recommender = BookRecommender()

        # Test user ID (make sure this user exists in your database)
        test_user_id = 1

        # Fetch user preferences to create relevant search queries
        user_prefs = recommender.get_user_preference_text(test_user_id)
        search_terms = user_prefs.split()[:3]  # Use first 3 preference terms

        # Fetch books from Google Books API
        all_books = []
        for term in search_terms:
            books = fetch_books_from_google_api(term)
            all_books.extend(process_google_books_response(books))

        # Get recommendations
        recommendations = recommender.get_recommendations(
            test_user_id,
            all_books,
            num_recommendations=5
        )

        # Print recommendations and debug information
        print("\nTop 5 Book Recommendations:")
        print("-" * 50)
        for i, rec in enumerate(recommendations, 1):
            book = rec['book']
            similarity = rec['similarity']
            print(f"\n{i}. {book['title']}")
            print(f"   Authors: {', '.join(book['authors'])}")
            print(f"   Similarity Score: {similarity:.2f}")
            print(f"   Categories: {', '.join(book['categories']) if book['categories'] else 'N/A'}")
            print(f"   Rating: {book['averageRating']}/5" if book['averageRating'] else "   Rating: N/A")
            if book['description']:
                print(f"   Description: {book['description'][:150]}...")

            # Debug similarity for each recommended book
            print("\nDebugging Similarity:")
            print("-" * 50)
            recommender.debug_similarity(test_user_id, book)

if __name__ == "__main__":
    test_recommendation_system()