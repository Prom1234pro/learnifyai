// document.addEventListener('DOMContentLoaded', function() {
//     document.getElementById('createGroupBtn').addEventListener('click', function() {
//       document.getElementById('groupPopup').style.display = 'block';
//     });
  
//     document.getElementsByClassName('close')[0].addEventListener('click', function() {
//       document.getElementById('groupPopup').style.display = 'none';
//     });
  
//     document.getElementById('groupForm').addEventListener('submit', function(e) {
//       e.preventDefault();
//       // Handle form submission here
//       // ...
//       // Close the popup after submission
//       document.getElementById('groupPopup').style.display = 'none';
//     });
//   });
  
  document.getElementById('exampleModal').addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget; // Button that triggered the modal
    var recipient = button.getAttribute('data-whatever'); // Extract info from data-* attributes
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. You could use other methods instead of jQuery.
    var modal = this;
    modal.querySelector('.modal-title').textContent = 'New message to ' + recipient;
    modal.querySelector('.modal-body input').value = recipient;
  });
  