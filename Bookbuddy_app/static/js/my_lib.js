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
    // Update book status to "current"
    fetch('/add-to-reading-list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            book_id: bookId,
            status: 'current'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success message
            alert(data.message);
            // Reload page to show updated lists
            window.location.reload();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
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