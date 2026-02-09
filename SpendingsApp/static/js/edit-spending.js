$(document).ready(function() {

    $("#edit-spending-form").validate({
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

    $('#edit-spending-api-button').mouseup(function(e) {
        e.preventDefault();
        if (!$("#edit-spending-form").valid()) {
            return;
        }
        editSpending();
    });

});

function editSpending() {
    const formElement = document.getElementById('edit-spending-form');
    const url = formElement?.dataset?.editUrl;

    if (!url) {
        console.error("Edit URL not found on form (data-edit-url).");
        alert("Cannot find edit URL. Check the page.");
        return;
    }

    const formData = new FormData(formElement);

    $.ajax({
        type: "POST",
        url: url,
        data: formData,
        processData: false,
        contentType: false,
        success: function(_data) {
     
        },
        error: function(xhr, _status, error) {
            console.error("Error status:", xhr.status);
            console.error("Error response:", xhr.responseText);
            console.error("Error message:", error);
            alert("Error editing spending. Please check the console.");
        }
    });
}