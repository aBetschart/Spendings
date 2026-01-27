
function updateRecentSpendings() {
    $.ajax({
        type: "POST",
        datatype: "json",
        contenttype: "application/json",
        data: {spendings_count: 10, csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
        url: DJANGO_URLS.spending_get_recent,
        success: function(data) {
            $('#table-spendings tbody').empty();

            var spendings = data.spendings;
            $.each(spendings, function(_index, spending) {
                var date = new Date(spending.spendingDate);
                var date_text = $.format.date(date, "dd.MM.yyyy")
                var amount_link = '<a class = "link-underline link-underline-opacity-0"' + 
                    'href="spending/edit/' + spending.id + '">' + spending.amount + '</a>';
                $('#table-spendings tbody').append(
                    '<tr>' + 
                    "<td class='text-nowrap text-truncate'>" + date_text + '</td>' + 
                    "<td class='text-nowrap text-truncate'>" + spending.category.name + '</td>' + 
                    "<td class='text-nowrap text-truncate'>" + spending.description + '</td>' + 
                    "<td class='text-end'>" + amount_link + '</td>' + 
                    '</tr>');              
            });
        }
    })
}

function postSpending() {

}

$(document).ready(function() {
    $("#submit-spending-form").validate({
        rules: {
            spendingDate: {
                required: true
            },
            description: {
                required: true,
                minlength: 2
            },
            amount: {
                required: true,
                number: true,
                min: 0.01
            },
            category: {
                required: true
            }
        },
        messages: {
            spendingDate: "Please enter a date",
            description: "Description is required (min 2 characters)",
            amount: "Please enter a valid amount (numeric greater than or equal 0.01)",
            category: "Please select a category"
        }
    });

    $('#submit-spending-api-btn').mouseup(function() {
        if ($("#submit-spending-form").valid()) {
            submitSpendingToAPI();
        }
    });
});

function submitSpendingToAPI() {
    var formData = new FormData(document.getElementById('submit-spending-form'));
    
    $.ajax({
        type: "POST",
        url: DJANGO_URLS.spending_submit_api,
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            console.log("Spending submitted successfully:", data);
            $("#submit-spending-form")[0].reset();
            updateRecentSpendings();
        },
        error: function(xhr, status, error) {
            console.error("Error status:", xhr.status);
            console.error("Error response:", xhr.responseText);
            console.error("Error message:", error);
            alert("Error submitting spending. Please check the console.");
        }
    });
}
