// Dummy quiz questions with options
const questions = [
    {
        question: "What is the capital of France?",
        options: ["Paris", "London", "Berlin", "Rome"],
        correctAnswer: "Paris"
    },
    {
        question: "What is 2 + 2?",
        options: ["3", "4", "5", "6"],
        correctAnswer: "4"
    },
    {
        question: "Who wrote 'To Kill a Mockingbird'?",
        options: ["Harper Lee", "J.K. Rowling", "Stephen King", "Mark Twain"],
        correctAnswer: "Harper Lee"
    }
];

let currentQuestionIndex = 0;

// Display current question
function displayQuestion() {
    const questionContainer = document.querySelector('.container');
    const currentQuestion = questions[currentQuestionIndex];
    
    let optionsHTML = '';
    currentQuestion.options.forEach((option, index) => {
        optionsHTML += `<input type="radio" name="answer" value="${option}" id="option${index}">`;
        optionsHTML += `<label for="option${index}">${option}</label><br>`;
    });
    
    questionContainer.innerHTML = `
        <h1>Quiz</h1>
        <p>${currentQuestion.question}</p>
        <form id="quiz-form">
            ${optionsHTML}
        </form>
        <button id="prev-btn" onclick="prevQuestion()">Previous</button>
        <button id="next-btn" onclick="checkAnswer()">Next</button>
    `;
}

// Go to previous question
function prevQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
}

// Check selected answer
function checkAnswer() {
    const selectedAnswer = document.querySelector('input[name="answer"]:checked');
    if (selectedAnswer) {
        const answerValue = selectedAnswer.value;
        const correctAnswer = questions[currentQuestionIndex].correctAnswer;
        if (answerValue === correctAnswer) {
            alert("Correct answer!");
        } else {
            alert("Incorrect answer!");
        }
        // Go to next question
        if (currentQuestionIndex < questions.length - 1) {
            currentQuestionIndex++;
            displayQuestion();
        } else {
            alert("End of quiz!");
        }
    } else {
        alert("Please select an answer.");
    }
}

// Initial display
displayQuestion();
