function showresult(yourScore)
{
    $('.loadingresult').css('display', 'grid');

    setTimeout(function()
    {
        $('.result_page').addClass('result_page_show');
        $('.u_score').html(yourScore + '%');
        $('.u_result_ span').html(yourScore + ' Points');

        if (yourScore >= 80) {
            $('.pass_check').html('<i class="fa-solid fa-check"></i> You Passed!');
            $('.result_msg').html('You passed the test!');
        }
        // $('.result_page').addClass('result_page_show');

    },1000)
};

$(document).ready(function () {
    let groupId, groupKey;
    console.log("here")
      $('#joingroup').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        groupId = button.data('groupid'); // Extract group ID from data-groupid attribute
        groupKey = button.data('groupkey'); // Extract group ID from data-groupid attribute
        var modal = $(this);
        // Set the value of the hidden input field in the modal form to the group ID
        modal.find('#group-access').val(groupKey);
        console.log(groupId)
    });
});
        
        
//correct answers
var correct_answers = ['Hong Kong','All of the above','Zoroastrianism','Gen. K.M. Cariappa', 'Zinc'];

// user answers
let correct = 0;

var steps = $('section').length;



console.log(steps);
function countresult(resultnumber)
{
    $('#step'+resultnumber+' .radio-field input').each(function()
    {
        for(var i = 0; i<=correct_answers.length; i++)
        {
            if($(this).is(':checked'))
        {
            if($(this).val() == correct_answers[i])
            {
                
    
                correct++;

                break;
    
            }
        }
        }
    
    })

    var correctprcnt = correct / steps * 100;

    $('.u_prcnt').html(correctprcnt + '%');
    $('.u_result span').html(correctprcnt + ' Points');

    if(correctprcnt >=80)
    {
        $('.pass_check').html('<i class="fa-solid fa-check"></i> You Passed!');
        $('.result_msg').html('You passed the test!');
    }
}
