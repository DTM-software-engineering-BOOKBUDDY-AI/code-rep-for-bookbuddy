let currentQuestion = 1;
const totalQuestions = 6; // Update if more questions are added

function showNextQuestion() {
    // Hide the current question
    document.getElementById(`question-${currentQuestion}`).classList.remove('active');

    // Increment the current question number
    currentQuestion++;

    // If there are more questions, show the next one
    if (currentQuestion <= totalQuestions) {
        document.getElementById(`question-${currentQuestion}`).classList.add('active');
    } else {
        // If no more questions, show recommendations
        document.getElementById('recommendations').classList.add('active');
    }
}

// Initialize: show the first question
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('question-1').classList.add('active');
});

