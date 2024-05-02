document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('createGroupBtn').addEventListener('click', function() {
      document.getElementById('groupPopup').style.display = 'block';
    });
  
    document.getElementsByClassName('close')[0].addEventListener('click', function() {
      document.getElementById('groupPopup').style.display = 'none';
    });
  
    document.getElementById('groupForm').addEventListener('submit', function(e) {
      e.preventDefault();
      // Handle form submission here
      // ...
      // Close the popup after submission
      document.getElementById('groupPopup').style.display = 'none';
    });
  });
  
