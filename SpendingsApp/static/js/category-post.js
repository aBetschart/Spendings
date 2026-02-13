import { validateCategoryForm } from './category-form-validate.js';
import { categoryTableUpdate } from './category-table-update.js';

$(document).ready(function() {

    validateCategoryForm("#category-post-form");

    $("#category-submit-btn").mouseup(function(e) {
        e.preventDefault();
        if (!$("#category-post-form").valid())
            return;

        const formElement = document.getElementById('category-post-form');
        const formData = new FormData(formElement);

        $.ajax({
            type: "POST",
            url: formElement.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(_data) {
                formElement.reset();
                categoryTableUpdate();
            },
            error: function(xhr, _status, error) {
                console.error("Error status:", xhr.status);
                console.error("Error response:", xhr.responseText);
                console.error("Error message:", error);
                alert("Error adding category. Please check the console.");
            }
        });   
    });

});