
import { validateCategoryForm } from "./category-form-validate.js";

$(document).ready(function() {
    validateCategoryForm("#category-form");
});

$("#category-form").submit(function(event) {
    event.preventDefault();

    const $form = $(this);

    if (typeof $form.valid === 'function' && !$form.valid()) 
        return;
    

    const formData = new FormData(this);
    const url = $form.attr("url");

    $.ajax({
        type: "POST",
        url: url,
        data: formData,
        processData: false,
        contentType: false
    }).done(function(_data) {
        // location.reload();
    }).fail(function(xhr, _status, error) {
        console.error("Error status:", xhr.status);
        console.error("Error response:", xhr.responseText);
        console.error("Error message:", error);
        alert("Error editing category. Please check the console.");
    });
});
