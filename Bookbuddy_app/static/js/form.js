let currentQuestion = 1;
const totalQuestions = 8;

function showLoading() {
    const submitButton = document.querySelector('.submit-button');
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = 'Getting Your Books...';
    }
}

function showNextQuestion() {
    // Validate current question (optional)
    if (!validateCurrentQuestion()) {
        return;
    }

    // Hide current question
    const currentQuestionElement = document.getElementById(`question-${currentQuestion}`);
    if (currentQuestionElement) {
        currentQuestionElement.classList.remove('active');
    }

    // Move to next question
    currentQuestion++;

    // Show next question or recommendations
    if (currentQuestion <= totalQuestions) {
        const nextQuestionElement = document.getElementById(`question-${currentQuestion}`);
        if (nextQuestionElement) {
            nextQuestionElement.classList.add('active');
        }
    } else {
        // Show recommendations section
        const recommendationsElement = document.getElementById('recommendations');
        if (recommendationsElement) {
            recommendationsElement.classList.add('active');
        }
    }
}

function validateCurrentQuestion() {
    const currentQuestionElement = document.getElementById(`question-${currentQuestion}`);
    if (!currentQuestionElement) return true;

    // Get all inputs in current question
    const inputs = currentQuestionElement.querySelectorAll('input[type="radio"], input[type="checkbox"], input[type="number"]');
    let isValid = false;

    // Check if at least one option is selected
    inputs.forEach(input => {
        if (input.type === 'radio' || input.type === 'checkbox') {
            if (input.checked) isValid = true;
        } else if (input.type === 'number') {
            if (input.value !== '') isValid = true;
        }
    });

    // Show error message if nothing is selected
    if (!isValid) {
        alert('Please select at least one option before proceeding.');
        return false;
    }

    return true;
}

// Initialize the form
document.addEventListener('DOMContentLoaded', function() {
    // Show first question
    const firstQuestion = document.getElementById('question-1');
    if (firstQuestion) {
        firstQuestion.classList.add('active');
    }

    // Add form submission handler
    const form = document.getElementById('book-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            showLoading();
            
            // Submit the form normally
            form.submit();
        });
    }
});

