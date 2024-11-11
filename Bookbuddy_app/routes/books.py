from flask import Blueprint, jsonify, request, current_app, render_template, flash, redirect, url_for
from services.google_books import GoogleBooksAPI

books_bp = Blueprint('books', __name__)

def get_books_api():
    """Get or create GoogleBooksAPI instance"""
    if not hasattr(current_app, 'books_api'):
        current_app.books_api = GoogleBooksAPI(current_app.config['GOOGLE_BOOKS_API_KEY'])
    return current_app.books_api

@books_bp.route('search', methods=['GET'])
def search_books():
    query = request.args.get('q', '')
    try:
        books_api = get_books_api()
        books = books_api.search_books(query)
        return jsonify(books)
    except Exception as e:
        print(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@books_bp.route('/book/<book_id>', methods=['GET'])
def get_book_details(book_id):
    try:
        books_api = get_books_api()
        book = books_api.get_book_details(book_id)
        return jsonify(book)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/search/results')
def search_results():
    query = request.args.get('q', '')
    if not query:
        flash('Please enter a search term', 'warning')
        return redirect(url_for('homepage'))
        
    try:
        books_api = get_books_api()
        books = books_api.search_books(query, max_results=20)
        return render_template('search_results.html', 
                             books=books, 
                             query=query)
    except Exception as e:
        flash(f'Error searching books: {str(e)}', 'error')
        return render_template('search_results.html', 
                             books=[], 
                             query=query)
@books_bp.route('/book/<book_id>')
def book_details(book_id):
    try:
        books_api = get_books_api()
        book = books_api.get_book_details(book_id)
        return render_template('book_details.html', book=book)
    except Exception as e:
        flash('Error fetching book details', 'error')
        return redirect(url_for('index'))

@books_bp.route('/preview/<book_id>')
def book_preview(book_id):
    try:
        books_api = get_books_api()
        book = books_api.get_book_details(book_id)
        
        if not book.get('preview_link'):
            flash('Preview not available for this book', 'warning')
            return redirect(url_for('books.book_details', book_id=book_id))
            
        return render_template('book_preview.html', book=book)
    except Exception as e:
        flash('Error loading book preview', 'error')
        return redirect(url_for('books.book_details', book_id=book_id))