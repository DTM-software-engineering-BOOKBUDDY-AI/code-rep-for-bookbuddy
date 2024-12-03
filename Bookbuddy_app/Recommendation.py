from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from models import User, UserPreferences
from extensions import db
from app import app  # Import your Flask app

class BookRecommender:
    def __init__(self):
        # Get all user preferences from database
        self.preferences = UserPreferences.query.all()
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def get_weighted_text(self, text, weight, feature_name):
        """Repeat text to give it more weight in similarity calculation"""
        return f"{feature_name}: {' '.join([text] * weight)}"

    def get_user_preference_text(self, user_id):
        """Convert user preferences into a text string with meaningful features"""
        preference = UserPreferences.query.filter_by(user_id=user_id).first()
        if not preference:
            return ""
        
        features = []
        
        # Give genres higher weight (repeat 3 times)
        if preference.genres:
            features.append(self.get_weighted_text(preference.genres, 3, 'genres'))
        
        # Theme and mood get medium weight (repeat 2 times)
        if preference.theme:
            features.append(self.get_weighted_text(preference.theme, 2, 'theme'))
        if preference.mood:
            features.append(self.get_weighted_text(preference.mood, 2, 'mood'))
        
        # Other features get normal weight
        if preference.language:
            features.append(f"language: {preference.language}")
        if preference.length:
            features.append(f"length: {preference.length}")
        if preference.maturity:
            features.append(f"maturity: {preference.maturity}")
        
        return ' '.join(features).lower()

    def get_book_text(self, book_data):
        """Convert book data into text with corresponding features"""
        features = []
        
        # Match the weighting from user preferences
        if book_data.get('categories'):
            features.append(self.get_weighted_text(' '.join(book_data['categories']), 3, 'genres'))
        
        # Description (can match with user's theme/mood preferences)
        if book_data.get('description'):
            features.append(self.get_weighted_text(book_data['description'], 2, 'theme'))
        
        # Language (direct match with user's language preference)
        if book_data.get('language'):
            features.append(f"language: {book_data['language']}")
        
        # Page count (corresponds to user's length preference)
        if book_data.get('pageCount'):
            page_count = book_data['pageCount']
            length_category = 'short' if page_count < 200 else 'medium' if page_count < 400 else 'long'
            features.append(f"length: {length_category}")
        
        # Maturity rating
        if book_data.get('maturityRating'):
            features.append(f"maturity: {book_data['maturityRating']}")
        
        return ' '.join(features).lower()

    def calculate_similarity(self, user_id, book_data):
        """Calculate similarity between user preferences and a book"""
        try:
            # Get user preferences as text
            user_text = self.get_user_preference_text(user_id)
            if not user_text.strip():
                return 0.0

            # Get book information as text
            book_text = self.get_book_text(book_data)
            if not book_text.strip():
                return 0.0

            # Create new vectorizer instance for each comparison
            vectorizer = TfidfVectorizer(stop_words='english',
                                         min_df=1,
                                         analyzer='word',
                                         token_pattern=r'\b\w+\b')

            # Fit and transform both texts
            try:
                tfidf_matrix = vectorizer.fit_transform([user_text, book_text])

                # Check if we have enough features
                if tfidf_matrix.shape[1] == 0:
                    return 0.0

                # Calculate cosine similarity
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
                return float(similarity[0][0])

            except ValueError as ve:
                print(f"Vectorization error: {str(ve)}")
                return 0.0

        except Exception as e:
            print(f"Error calculating similarity: {str(e)}")
            return 0.0

    def get_recommendations(self, user_id, book_list, num_recommendations=5):
        """Get top N book recommendations for a user from a list of books"""
        try:
            similarities = []

            for book in book_list:
                similarity = self.calculate_similarity(user_id, book)
                similarities.append({
                    'book': book,
                    'similarity': similarity
                })

            # Sort by similarity score
            sorted_recommendations = sorted(
                similarities,
                key=lambda x: x['similarity'],
                reverse=True
            )

            # Return top N recommendations
            return sorted_recommendations[:num_recommendations]

        except Exception as e:
            print(f"Error getting recommendations: {str(e)}")
            return []

    def debug_similarity(self, user_id, book_data):
        """Debug method to see how features are matching"""
        user_text = self.get_user_preference_text(user_id)
        book_text = self.get_book_text(book_data)
        
        print("\nUser Preferences:")
        print("-" * 50)
        print(user_text)
        print("\nBook Features:")
        print("-" * 50)
        print(book_text)
        print("\nSimilarity Score:", self.calculate_similarity(user_id, book_data))

# Example usage
if __name__ == "__main__":
    # Create recommender instance
    recommender = BookRecommender()

    # Example book data (similar to what you might get from Google Books API)
    sample_book = {
        'categories': ['Fiction', 'Fantasy'],
        'description': 'A magical adventure story...',
        'authors': ['J.K. Rowling'],
        'language': 'en'

    }

    # Calculate similarity for a specific user and book
    user_id = 1  # Replace with actual user ID
    similarity = recommender.calculate_similarity(user_id, sample_book)
    print(f"Similarity score: {similarity}")