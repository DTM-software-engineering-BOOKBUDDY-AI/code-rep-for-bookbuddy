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
    const preview = document.getElementById("summary-preview");

    // If the full summary is hidden, show it and expand the preview box
    if (fullSummary.classList.contains("hidden")) {
        fullSummary.classList.remove("hidden");
        preview.style.whiteSpace = "normal"; // Remove single-line truncation
        preview.style.textOverflow = "clip"; // Remove "..."
    } else {
        fullSummary.classList.add("hidden");
        preview.style.whiteSpace = "nowrap"; // Restore truncation
        preview.style.textOverflow = "ellipsis"; // Restore "..."
    }
}
