from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from extensions import db
from models import Book

reading_list_bp = Blueprint('reading_list', __name__)

@reading_list_bp.route('/add/<int:book_id>', methods=['POST'])
@login_required
def add_to_reading_list(book_id):
    book = Book.query.get_or_404(book_id)
    current_user.add_to_reading_list(book)
    return jsonify({'status': 'success'})

@reading_list_bp.route('/update/<int:book_id>', methods=['POST'])
@login_required
def update_reading_status(book_id):
    book = Book.query.get_or_404(book_id)
    status = request.json.get('status')
    progress = request.json.get('progress')
    current_user.update_reading_status(book, status, progress)
    return jsonify({'status': 'success'}) 