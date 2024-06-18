// creating an array and passing the number, questions, options, and answers
let questions 

document.addEventListener('DOMContentLoaded', function() {
  const startButton = document.querySelector('.start_btn button');

  startButton.addEventListener('click', function() {
    console.log(this.parentElement.getAttribute('data-quiz'))
      const quizDataString = Array(this.parentElement.getAttribute('data-quiz'));
      const quizData = JSON.parse(quizDataString)
      console.log(quizData)
      questions = quizData.map((quiz, index) => {
          return {
              numb: index + 1,
              subject: quiz.subject,
              topic: quiz.topic,
              question: quiz.question_text,
              answer: quiz.options.find(option => option.is_correct).option_text,
              options: quiz.options.map(option => option.option_text)
          };
      });

      // Now you can use the 'questions' array for your quiz logic
      console.log(questions);

      // For example, you can start the quiz here
      startQuiz(questions);
  });

  function startQuiz(questions) {
      // Your logic to start the quiz using the 'questions' array
      console.log("Quiz started with questions:", questions);
  }
});
