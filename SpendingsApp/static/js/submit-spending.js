$(document).ready(function() {
    validateSpendingForm("#submit-spending-form");

    $('#submit-spending-api-btn').mouseup(function() {
        if ($("#submit-spending-form").valid()) {
            submitSpending();
        }
    });
});

function submitSpending() {
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
