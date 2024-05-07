document.querySelectorAll('.form input, .form textarea').forEach(function(element) {
    element.addEventListener('keyup', function(e) {
        var label = this.previousElementSibling;
        if (this.value === '') {
            label.classList.remove('active', 'highlight');
        } else {
            label.classList.add('active', 'highlight');
        }
    });

    element.addEventListener('blur', function(e) {
        var label = this.previousElementSibling;
        if (this.value === '') {
            label.classList.remove('active', 'highlight');
        } else {
            label.classList.remove('highlight');
        }
    });

    element.addEventListener('focus', function(e) {
        var label = this.previousElementSibling;
        if (this.value === '') {
            label.classList.remove('highlight');
        } else {
            label.classList.add('highlight');
        }
    });
});

document.querySelectorAll('.tab a').forEach(function(element) {
    element.addEventListener('click', function(e) {
        e.preventDefault();

        var parent = this.parentElement;
        parent.classList.add('active');
        var siblings = parent.parentElement.children;
        for (var i = 0; i < siblings.length; i++) {
            if (siblings[i] !== parent) {
                siblings[i].classList.remove('active');
            }
        }

        var target = this.getAttribute('href');
        document.querySelectorAll('.tab-content > div').forEach(function(content) {
            if (content !== target) {
                content.style.display = 'none';
            }
        });

        document.querySelector(target).style.display = 'block';
    });
});
