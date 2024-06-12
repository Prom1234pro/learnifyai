var divs = $('.show-section section');
var now = 0; // currently shown div
divs.hide().first().show(); // hide all divs except first


var count = 60;

var interval = setInterval(function() 
{
  
  if(count == 0)
  {
    clearInterval(interval);
  }
  else 
  {
    count = count -1;
  }
  document.getElementById("countdown-timer").innerHTML = count;
},1000);

$(document).ready(function() {
    var divs = $('.show-section section');
    var progress = $('#progressBar');
    var now = 0;
    var correctOptions = [];
    var wrongOptions = [];


    function next() {
        divs.eq(now).hide();
        now = (now + 1 < divs.length) ? now + 1 : 0;
        divs.eq(now).show();
        var progressPercentage = (now + 1) / divs.length * 100;
        progress.css('width', progressPercentage + '%');
    }

    function prev() {
        divs.eq(now).hide();
        now = (now > 0) ? now - 1 : divs.length - 1;
        divs.eq(now).show();
        var progressPercentage = (now + 1) / divs.length * 100;
        progress.css('width', progressPercentage + '%');
    }

    $(".next").on('click', function() {
        next();
    });

    $(".prev").on('click', function() {
        prev();
    });
    $("#backtocourses").on('click', function() {
        var course_id = $(this).data('course_id');
        window.location.href = '/courses/'+course_id; // Update the URL to your course page
    });
    
    function resultFunction() {
        var correctOptions = [];
        var wrongOptions = [];
        var allRadioInputs = $('input[type="radio"]');
        allRadioInputs.each(function() {
            var checkedRadio = $(this);
            console.log("submit clicked here");
            var optionId = checkedRadio.val();
            var correct = checkedRadio.data('correct');
            if (checkedRadio.prop('checked')) {
                if (correct === "True") {
                    correctOptions.push(optionId);
                } else {
                    wrongOptions.push(optionId);
                }
            }
        });
        var totalQuestions = allRadioInputs.length;
        var totalCorrect = correctOptions.length;
        console.log(totalQuestions);
        var totalScore = Math.floor((totalCorrect / totalQuestions) * 100);
        $('.u_score').html("Your Score: " + totalCorrect);
        $('.u_prcnt').html("Average: " + totalScore + '%');
        $('.u_result span').html(totalScore + ' Points');
    
        if (totalScore >= 80) {
            $('.pass_check').html('<i class="fa-solid fa-check pass"></i> You Passed!');
            $('.result_msg').html('You passed the test!');
        }
    
        correctOptions = [];
        wrongOptions = [];
    
        // Update the performance score via AJAX
        var performanceId = 'YOUR_PERFORMANCE_ID'; // Replace with the actual performance ID
        $.ajax({
            url: '/updateperformance/' + performanceId,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                score: totalCorrect,
                average: totalScore,
                progress: 'some_progress_value' // Replace with actual progress value if needed
            }),
            success: function(response) {
                console.log('Performance updated:', response);
                // Optionally, handle the response, show success message, etc.
            },
            error: function(error) {
                console.error('Error updating performance:', error);
                // Optionally, handle the error, show error message, etc.
            }
        });
    }
    
    $(".submit").on('click', resultFunction);

    
    var hours = parseInt($("#hour").text());
    var minutes = parseInt($("#minutes").text());
    var seconds = parseInt($("#seconds").text());

    function updateCountdown() {
        if (seconds == 0 && minutes == 0 && hours == 0) {
            clearInterval(interval);
            resultFunction();
            //disable next and submit button here
            $(".next, .submit").prop("disabled", true);
            $('#resultModal').modal('show');
            return;
        }
        if (seconds == 0){
            seconds = 59;
            if(minutes == 0) {
                hours--;
                minutes = 59;
            }else {
                minutes--;
            }
        }else {
            seconds--;
        }
        $("#hour").text(hours);
        $("#minutes").text(minutes);
        $("#seconds").text(seconds);
    }

    var interval = setInterval(updateCountdown, 1000); // Update every minute

});


// function showresult(yourScore)
// {
//         $('.loadingresult').css('display', 'none');
//         $('.result_page').addClass('result_page_show');
//         $('.u_prcnt').html(yourScore + '%');
//         $('.u_result span').html(yourScore + ' Points');

//         if (yourScore >= 80) {
//             $('.pass_check').html('<i class="fa-solid fa-check"></i> You Passed!');
//             $('.result_msg').html('You passed the test!');
//         }
//         // $('.result_page').addClass('result_page_show');

// }