// Book Details Handler
function showBookDetails(bookId) {
    const modal = new bootstrap.Modal(document.getElementById('bookDetailsModal'));
    modal.show();
}

// Note Handler
function addNote(bookId) {
    const modal = new bootstrap.Modal(document.getElementById('addNoteModal'));
    // Set the book ID in a hidden input if needed
    document.getElementById('noteBookId').value = bookId;
    modal.show();
}

// Progress Handler
function updateProgress(bookId) {
    const modal = new bootstrap.Modal(document.getElementById('updateProgressModal'));
    // Set the book ID in a hidden input if needed
    document.getElementById('progressBookId').value = bookId;
    modal.show();
}

// Start Reading Handler
function startReading(bookId) {
    // Add logic to move book to currently reading
    alert('Book moved to currently reading list');
}

// Review Handler
function showReview(bookId) {
    // Add logic to show review
    alert('Review feature coming soon!');
}

// Save Note Handler
function saveNote() {
    const bookId = document.getElementById('noteBookId').value;
    const noteTitle = document.getElementById('noteTitle').value;
    const noteContent = document.getElementById('noteContent').value;
    
    // Here you would typically send this to your backend
    console.log('Saving note for book:', bookId, {title: noteTitle, content: noteContent});
    
    // Close the modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('addNoteModal'));
    modal.hide();
    
    // Show success message
    alert('Note saved successfully!');
} 