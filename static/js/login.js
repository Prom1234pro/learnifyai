document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();
    // Perform login process here (e.g., send data to server)
    // Redirect to login page after login
    window.location.href = "/";
});
