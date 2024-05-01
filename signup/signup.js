document.getElementById("signup-form").addEventListener("submit", function(event) {
    event.preventDefault();
    // Perform signup process here (e.g., send data to server)
    // Redirect to login page after signup
    window.location.href = "/login";
});
