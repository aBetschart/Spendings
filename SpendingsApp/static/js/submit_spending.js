
const SPENDING_DATE = '#id_spendingDate'
const DESCRIPTION = '#id_description'
const AMOUNT = '#id_amount'
const CATEGORY = '#id_category'

$('#spending-form').on('submit', function(event){
    event.preventDefault();
    submitSpending();
});

function submitSpending() {
    $.ajax({
        url : "spending/submit/api",
        type : "POST",
        data : { 
            spendingDate : $(SPENDING_DATE).val(),
            description : $(DESCRIPTION).val(),
            amount : $(AMOUNT).val(),
            category : $(CATEGORY).val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : function(response) {
            $(SPENDING_DATE).val('');
            $(DESCRIPTION).val('');
            $(AMOUNT).val('');
            $(CATEGORY).val('');
        },
        error : function(xhr,errmsg,err) {
            // TODO: add error handler here
            // $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            //     " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
