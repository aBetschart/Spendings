import { validateCategoryForm } from './category-form-validate.js';
import { categoryTableUpdate } from './category-table-update.js';

$(document).ready(function() {

    validateCategoryForm("#category-form");

    $("#category-submit-btn").on('click', function(e) {
        validateCategoryForm("#category-form");

        e.preventDefault();
        if (!$("#category-form").valid())
            return;

        const formElement = document.getElementById('category-form');
        if (!formElement) {
            console.error("category-post: form element with id 'category-form' not found");
            return;
        }
        const formData = new FormData(formElement);

        $.ajax({
            type: "POST",
            url: DJANGO_URLS.category_post,
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