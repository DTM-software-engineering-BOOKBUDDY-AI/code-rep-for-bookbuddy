# Import necessary tools to handle web requests and Google Books API
from flask import Blueprint, jsonify, request, current_app, render_template, flash, redirect, url_for
from services.google_books import GoogleBooksAPI

# Create a Blueprint for organizing book-related routes
# Think of this as a section of our website dedicated to book features
books_bp = Blueprint('books', __name__)

# Helper function to connect to Google Books API
def get_books_api():
    """Get or create a connection to Google Books"""
    # Check if we already have a connection
    if not hasattr(current_app, 'books_api'):
        # If not, create a new connection using our API key
        current_app.books_api = GoogleBooksAPI(current_app.config['GOOGLE_BOOKS_API_KEY'])
    return current_app.books_api

# Route for searching books (like using a library catalog)
@books_bp.route('search', methods=['GET'])
def search_books():
    # Get the search term from the user's request
    query = request.args.get('q', '')
    try:
        # Connect to Google Books and search
        books_api = get_books_api()
        books = books_api.search_books(query)
        # Return the results as JSON (a format computers can easily read)
        return jsonify(books)
    except Exception as e:
        # If something goes wrong, log the error and return an error message
        print(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Route for displaying search results in a web page
@books_bp.route('/search/results')
def search_results():
    # Get the search term
    query = request.args.get('q', '')
    if not query:
        # If no search term was provided, show a warning
        flash('Please enter a search term', 'warning')
        return redirect(url_for('homepage'))
        
    try:
        # Search for books (limit to 20 results)
        books_api = get_books_api()
        books = books_api.search_books(query, max_results=20)
        # Show the results page with the found books
        return render_template('search_results.html', 
                             books=books, 
                             query=query)
    except Exception as e:
        # If there's an error, show the results page with no books
        flash(f'Error searching books: {str(e)}', 'error')
        return render_template('search_results.html', 
                             books=[], 
                             query=query)

# Route for showing detailed book information page
@books_bp.route('/book/<book_id>')
def book_details(book_id):
    try:
        books_api = get_books_api()
        book = books_api.get_book_details(book_id)
        return render_template('book_details.html', book=book)
    except Exception as e:
        flash('Error fetching book details', 'error')
        return redirect(url_for('homepage'))

# Route for showing book preview (if available)
@books_bp.route('/preview/<book_id>')
def book_preview(book_id):
    try:
        # Get book details and check if preview is available
        books_api = get_books_api()
        book = books_api.get_book_details(book_id)
        
        # If no preview is available, show a warning
        if not book.get('preview_link'):
            flash('Preview not available for this book', 'warning')
            return redirect(url_for('books.book_details', book_id=book_id))
            
        # Show the preview page
        return render_template('book_preview.html', book=book)
    except Exception as e:
        # Handle any errors
        flash('Error loading book preview', 'error')
        return redirect(url_for('books.book_details', book_id=book_id))