// Image Slideshow Logic
let currentImageIndex = 0;
const images = [
    "https://covers.openlibrary.org/b/id/8224816-L.jpg", // Don Quixote
    "https://covers.openlibrary.org/b/id/8344849-L.jpg", // Another book cover as an example
];

function nextImage() {
    currentImageIndex = (currentImageIndex + 1) % images.length;
    document.getElementById("book-cover").src = images[currentImageIndex];
}

function prevImage() {
    currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
    document.getElementById("book-cover").src = images[currentImageIndex];
}

// Toggle Full Summary
function toggleSummary() {
    const fullSummary = document.getElementById("full-summary");
    const readMoreText = document.getElementById("read-more-text");
    const summaryIcon = document.getElementById("summary-icon");
    
    if (fullSummary.classList.contains("hidden")) {
        fullSummary.classList.remove("hidden");
        readMoreText.textContent = "Read Less";
        summaryIcon.classList.remove("fa-chevron-down");
        summaryIcon.classList.add("fa-chevron-up");
    } else {
        fullSummary.classList.add("hidden");
        readMoreText.textContent = "Read More";
        summaryIcon.classList.remove("fa-chevron-up");
        summaryIcon.classList.add("fa-chevron-down");
    }
}

// Add this to your existing JavaScript
const books = [
    {
        id: 1,
        title: "Don Quixote",
        author: "Miguel de Cervantes",
        cover: "https://covers.openlibrary.org/b/id/8224816-L.jpg",
        rating: "4.5",
        genre: "Novel",
        language: "Spanish",
        year: "1605",
        summary: "Don Quixote is a Spanish novel that follows the adventures of a noble who, after reading too many chivalric romances, loses his sanity...",
        fullSummary: "The story tells the adventures of a nobleman who reads so many chivalric romances that he loses his mind and decides to become a knight-errant, recruiting a simple farmer, Sancho Panza, as his squire..."
    },
    // Add more books as needed
];

let currentBookIndex = 0;

function updateBookDisplay() {
    const book = books[currentBookIndex];
    document.getElementById("book-cover").src = book.cover;
    document.getElementById("book-name").textContent = book.title;
    document.getElementById("book-author").textContent = `by ${book.author}`;
    document.querySelector(".stat-item:nth-child(1) span").textContent = book.rating;
    document.querySelector(".stat-item:nth-child(2) span").textContent = book.genre;
    document.querySelector(".stat-item:nth-child(3) span").textContent = book.language;
    document.querySelector(".stat-item:nth-child(4) span").textContent = book.year;
    
    // Update summary sections
    document.getElementById("summary-preview").innerHTML = `
        ${book.summary}
        <button class="btn btn-link btn-sm" onclick="toggleSummary()">
            <span id="read-more-text">Read More</span>
            <i class="fas fa-chevron-down" id="summary-icon"></i>
        </button>
    `;
    document.getElementById("full-summary").innerHTML = `<p>${book.fullSummary}</p>`;
    
    // Reset summary state
    document.getElementById("full-summary").classList.add("hidden");
}

function nextImage() {
    currentBookIndex = (currentBookIndex + 1) % books.length;
    updateBookDisplay();
}

function prevImage() {
    currentBookIndex = (currentBookIndex - 1 + books.length) % books.length;
    updateBookDisplay();
}

// Add this function to handle the More Details button
function showMoreDetails() {
    const book = books[currentBookIndex];
    window.location.href = book.detailsUrl;
}

// Add this function to handle navigation to details page
function goToDetails() {
    const book = books[currentBookIndex];
    window.location.href = `/book/details/${book.id}`;
}

// Initialize the display
document.addEventListener('DOMContentLoaded', function() {
    updateBookDisplay();
    
    // Add click handler for More Details button
    document.querySelector('.btn-outline-primary').addEventListener('click', showMoreDetails);
});

// Add some CSS for the transition
const style = document.createElement('style');
style.textContent = `
    #full-summary {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease-out;
    }

    #full-summary.hidden {
        max-height: 0;
    }

    #full-summary:not(.hidden) {
        max-height: 500px; /* Adjust based on your content */
    }
`;
document.head.appendChild(style);
