// Function to retrieve course information from URL query parameters
function getCourseFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('course');
}

// Function to display course content based on the selected course
function displayCourseContent(course) {
    const courseContentElement = document.getElementById('course-content');
    // You can implement logic here to fetch and display content based on the selected course
    courseContentElement.innerHTML = `<p>This is the course description of ${course}.</p>`;
}

// Function to navigate to the quiz page
function goToQuiz() {
    window.location.href = "quiz.html";
}

// Retrieve course information from URL and display course content
const selectedCourse = getCourseFromURL();
if (selectedCourse) {
    displayCourseContent(selectedCourse);
} else {
    // Handle case where no course is selected
    alert("No course selected!");
    window.location.href = "index.html";
}
