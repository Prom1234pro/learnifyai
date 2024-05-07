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

setTimeout(function()
{
    $('.step-single').eq(0).addClass('active show');

}, 800)






// quiz validation
var checkedradio = false;

function radiovalidate(stepnumber)
{
    var checkradio = $("#step"+stepnumber+" input").map(function()
    {
    if($(this).is(':checked'))
    {
        return true;
    }
    else
    {
        return false;
    }
    }).get();

    checkedradio = checkradio.some(Boolean);
}


$(document).ready(function() {
    var divs = $('.show-section section');
    var now = 0;
    var correctOptions = [];
    var wrongOptions = [];

    function showActiveStep() {
        $('.step-single').removeClass('show');
        $('.step-single').eq(now).addClass('active show');
    }

    function next() {
        divs.eq(now).hide();
        now = (now + 1 < divs.length) ? now + 1 : 0;
        divs.eq(now).show();
        showActiveStep();
    }

    function prev() {
        divs.eq(now).hide();
        now = (now > 0) ? now - 1 : divs.length - 1;
        divs.eq(now).show();
        showActiveStep();
    }

    $(".next").on('click', function() {
        next();
    });

    $(".prev").on('click', function() {
        prev();
    });

    $("#submit").on('click', function() {
        // Perform form validation
        var allRadioInputs = $('input[type="radio"]');
        allRadioInputs.each(function() {
            var checkedRadio = $(this);
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
    });

    $("#submit").on('click', function() {
        // Calculate total score
        var totalQuestions = divs.length;
        var totalCorrect = correctOptions.length;
        console.log(totalQuestions, totalCorrect);
        var totalScore = (totalCorrect / totalQuestions) * 100;
        console.log("Total Score: " + totalScore);
        correctOptions = [];
        wrongOptions = [];
        showresult(totalScore);
    });

    // Countdown timer logic
    var count = 60;
    var interval = setInterval(function() {
        count = (count > 0) ? count - 1 : 0;
        $("#countdown-timer").text(count);
        if (count == 0) {
            clearInterval(interval);
            // Automatically submit the form when timer reaches 0
            $("#quizForm").submit();
        }
    }, 1000);
});
