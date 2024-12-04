document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    let currentBookIndex = 0;
    const slides = document.querySelectorAll('.book-slide');
    const totalBooks = slides.length;

    // Show initial book
    if (totalBooks > 0) {
        showBook(0);
    }

    // Add event listeners for arrow keys
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            prevBook();
        } else if (e.key === 'ArrowRight') {
            nextBook();
        }
    });
});

// Make functions globally available
function showBook(index) {
    const slides = document.querySelectorAll('.book-slide');
    slides.forEach(slide => {
        slide.style.display = 'none';
    });
    slides[index].style.display = 'block';
    currentBookIndex = index;
}

function nextBook() {
    const slides = document.querySelectorAll('.book-slide');
    currentBookIndex = (currentBookIndex + 1) % slides.length;
    showBook(currentBookIndex);
}

function prevBook() {
    const slides = document.querySelectorAll('.book-slide');
    currentBookIndex = (currentBookIndex - 1 + slides.length) % slides.length;
    showBook(currentBookIndex);
}

function toggleSummary(index) {
    const slide = document.querySelector(`.book-slide[data-index="${index}"]`);
    const fullSummary = slide.querySelector('.full-summary');
    const icon = slide.querySelector('.summary-icon');
    const text = slide.querySelector('.read-more-text');
    
    if (fullSummary.classList.contains('hidden')) {
        fullSummary.classList.remove('hidden');
        icon.classList.remove('fa-chevron-down');
        icon.classList.add('fa-chevron-up');
        text.textContent = 'Read Less';
    } else {
        fullSummary.classList.add('hidden');
        icon.classList.remove('fa-chevron-up');
        icon.classList.add('fa-chevron-down');
        text.textContent = 'Read More';
    }
}

function addToReadingList(bookId) {
    fetch('/add-to-reading-list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrf_token') // Add CSRF token if needed
        },
        body: JSON.stringify({ book_id: bookId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Book added to reading list successfully!');
        } else {
            alert(data.message || 'Error adding book to reading list');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error adding book to reading list');
    });
}

function viewBookDetails(bookId) {
    window.location.href = `/book/${bookId}`;
}

// Helper function to get CSRF token if needed
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Add touch support for mobile devices
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    const swipeThreshold = 50;
    const swipeLength = touchEndX - touchStartX;

    if (Math.abs(swipeLength) > swipeThreshold) {
        if (swipeLength > 0) {
            prevBook();
        } else {
            nextBook();
        }
    }
}
