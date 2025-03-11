// Book Details Handler
function showBookDetails(bookId) {
    console.log("showBookDetails called with bookId:", bookId);
    
    // Get book details from data attributes
    const bookCard = document.querySelector(`[data-book-id="${bookId}"]`);
    if (!bookCard) {
        console.error("No book card found with data-book-id:", bookId);
        showToast('Error: Could not find book details', 'danger');
        return;
    }
    
    const bookTitle = bookCard.dataset.title;
    const bookAuthor = bookCard.dataset.author;
    const bookCover = bookCard.dataset.cover;
    
    console.log("Found book card with data:", { 
        title: bookTitle, 
        author: bookAuthor, 
        cover: bookCover 
    });
    
    // Set modal content
    document.getElementById('modalBookTitle').textContent = bookTitle;
    document.getElementById('modalBookAuthor').textContent = bookAuthor;
    
    // Set cover image if available
    const coverImg = document.getElementById('modalBookCover');
    if (coverImg) {
        coverImg.src = `/static/images/products/${bookCover}`;
        coverImg.alt = bookTitle;
    }
    
    const modal = new bootstrap.Modal(document.getElementById('bookDetailsModal'));
    modal.show();
}

// Note Handler
function addNote(bookId) {
    console.log("addNote called with bookId:", bookId);
    
    // Get book details from data attributes
    const bookCard = document.querySelector(`[data-book-id="${bookId}"]`);
    if (!bookCard) {
        console.error("No book card found with data-book-id:", bookId);
        showToast('Error: Could not find book details', 'danger');
        return;
    }
    
    // Set the book ID in the hidden input
    document.getElementById('noteBookId').value = bookId;
    
    // Set book title in the modal if available
    const modalTitle = document.querySelector('#addNoteModal .modal-title');
    if (modalTitle) {
        modalTitle.textContent = `Add Note for "${bookCard.dataset.title}"`;
    }
    
    const modal = new bootstrap.Modal(document.getElementById('addNoteModal'));
    modal.show();
}

// Progress Handler
function updateProgress(bookId) {
    console.log("updateProgress called with bookId:", bookId);
    
    // Get book details from data attributes
    const bookCard = document.querySelector(`[data-book-id="${bookId}"]`);
    if (!bookCard) {
        console.error("No book card found with data-book-id:", bookId);
        showToast('Error: Could not find book details', 'danger');
        return;
    }
    
    // Set the book ID in the hidden input
    document.getElementById('progressBookId').value = bookId;
    
    // Set book title in the modal if available
    const modalTitle = document.querySelector('#updateProgressModal .modal-title');
    if (modalTitle) {
        modalTitle.textContent = `Update Progress for "${bookCard.dataset.title}"`;
    }
    
    const modal = new bootstrap.Modal(document.getElementById('updateProgressModal'));
    modal.show();
}

// Start Reading Handler
function startReading(bookId) {
    console.log("startReading called with bookId:", bookId);
    
    // Get book details from data attributes
    const bookCard = document.querySelector(`[data-book-id="${bookId}"]`);
    if (!bookCard) {
        console.error("No book card found with data-book-id:", bookId);
        showToast('Error: Could not find book details', 'danger');
        return;
    }
    
    const bookTitle = bookCard.dataset.title;
    const bookAuthor = bookCard.dataset.author;
    const bookCover = bookCard.dataset.cover;
    
    console.log("Found book card with data:", { 
        title: bookTitle, 
        author: bookAuthor, 
        cover: bookCover 
    });
    
    // Show loading indicator
    const loadingToast = showToast('Adding book to your reading list...', 'info', false);
    
    const requestData = {
        book_id: bookId,
        status: 'current',
        title: bookTitle || 'Unknown Title',
        author: bookAuthor || 'Unknown Author',
        cover_image: bookCover || 'default-book-cover.jpg'
    };
    
    console.log("Sending request with data:", requestData);
    
    // Update book status to "current"
    fetch('/add-to-reading-list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        console.log("Response status:", response.status);
        return response.json();
    })
    .then(data => {
        console.log("Response data:", data);
        
        // Hide loading toast
        if (loadingToast) {
            loadingToast.hide();
        }
        
        if (data.success) {
            // Show success message
            showToast(data.message, 'success');
            // Reload page to show updated lists
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            console.error("Error from server:", data.message);
            showToast('Error: ' + data.message, 'danger');
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        
        // Hide loading toast
        if (loadingToast) {
            loadingToast.hide();
        }
        
        showToast('An error occurred. Please try again.', 'danger');
    });
}

// Helper function to show toast notifications
function showToast(message, type = 'info', autohide = true) {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    
    // Toast content
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Add to container
    toastContainer.appendChild(toastEl);
    
    // Initialize Bootstrap toast
    const toast = new bootstrap.Toast(toastEl, {
        autohide: autohide,
        delay: 5000
    });
    
    // Show toast
    toast.show();
    
    // Return toast instance for later use
    return toast;
}

// Review Handler
function showReview(bookId) {
    console.log("showReview called with bookId:", bookId);
    
    // Get book details from data attributes
    const bookCard = document.querySelector(`[data-book-id="${bookId}"]`);
    if (!bookCard) {
        console.error("No book card found with data-book-id:", bookId);
        showToast('Error: Could not find book details', 'danger');
        return;
    }
    
    // For now, just show a toast notification
    showToast(`Review feature for "${bookCard.dataset.title}" coming soon!`, 'info');
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