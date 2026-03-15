
$(document).on('click', '.delete-category-btn', function() {
    const categoryId = $(this).data('category-id');
    const fadeOutDuration = 300;
    $.ajax({
        type: "POST",
        url: `category/delete/${categoryId}`,
        data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
        success: function(_response) {
            const table_row = $(`button[data-category-id='${categoryId}']`).closest('tr');
            table_row.fadeOut(fadeOutDuration, function() {
                $(this).remove();
            });
        },
        error: function(_xhr, _status, error) {
            alert(`Error deleting category: ${error}`);
        }
    })
});