import requests
from cachetools import TTLCache
from flask import current_app
import logging

logger = logging.getLogger(__name__)

# Cache for storing book data (1000 items, 1 hour timeout)
book_cache = TTLCache(maxsize=1000, ttl=3600)

class GoogleBooksAPI:
    BASE_URL = "https://www.googleapis.com/books/v1"
    
    def __init__(self, api_key):
        self.api_key = api_key
    
    def search_books(self, query, max_results=10):
        """Search for books using the Google Books API"""
        try:
            # Check cache first
            cache_key = f"search_{query}_{max_results}"
            if cache_key in book_cache:
                return book_cache[cache_key]
            
            params = {
                'q': query,
                'maxResults': max_results,
                'key': self.api_key
            }
            
            response = requests.get(f"{self.BASE_URL}/volumes", params=params)
            response.raise_for_status()
            
            data = response.json()
            books = self._parse_books(data.get('items', []))
            
            # Cache the results
            book_cache[cache_key] = books
            return books
            
        except requests.RequestException as e:
            logger.error(f"Error searching books: {str(e)}")
            raise
    
    def get_book_details(self, book_id):
        """Get detailed information about a specific book"""
        try:
            # Check cache first
            cache_key = f"book_{book_id}"
            if cache_key in book_cache:
                return book_cache[cache_key]
            
            response = requests.get(
                f"{self.BASE_URL}/volumes/{book_id}",
                params={'key': self.api_key}
            )
            response.raise_for_status()
            
            book_data = response.json()
            book_details = self._parse_book_details(book_data)
            
            # Cache the results
            book_cache[cache_key] = book_details
            return book_details
            
        except requests.RequestException as e:
            logger.error(f"Error fetching book details: {str(e)}")
            raise
    
    def _parse_books(self, items):
        """Parse book data from API response"""
        books = []
        for item in items:
            try:
                volume_info = item.get('volumeInfo', {})
                books.append({
                    'id': item.get('id'),
                    'title': volume_info.get('title'),
                    'authors': volume_info.get('authors', []),
                    'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail'),
                    'preview_link': volume_info.get('previewLink'),
                    'published_date': volume_info.get('publishedDate'),
                    'description': volume_info.get('description', '')[:200] + '...'
                })
            except Exception as e:
                logger.error(f"Error parsing book data: {str(e)}")
                continue
        return books
    
    def _parse_book_details(self, data):
        """Parse detailed book information"""
        volume_info = data.get('volumeInfo', {})
        return {
            'id': data.get('id'),
            'title': volume_info.get('title'),
            'authors': volume_info.get('authors', []),
            'publisher': volume_info.get('publisher'),
            'published_date': volume_info.get('publishedDate'),
            'description': volume_info.get('description'),
            'page_count': volume_info.get('pageCount'),
            'categories': volume_info.get('categories', []),
            'rating': volume_info.get('averageRating'),
            'ratings_count': volume_info.get('ratingsCount'),
            'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail'),
            'preview_link': volume_info.get('previewLink'),
            'isbn_13': next((id['identifier'] for id in volume_info.get('industryIdentifiers', [])
                           if id['type'] == 'ISBN_13'), None)
        } 