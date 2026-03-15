

$(document).on('click', '.delete-spending-btn', function() {
    const spendingId = $(this).data('spending-id');
    const fadeOutDuration = 300;
    $.ajax({
        type: "POST",
        url: `spending/delete/api/${spendingId}`,
        data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
        success: function(_response) {
            const table_row = $(`button[data-spending-id='${spendingId}']`).closest('tr');
            table_row.fadeOut(fadeOutDuration, function() {
                $(this).remove();
            });
        },
        error: function(_xhr, _status, error) {
            alert(`Error deleting spending: ${error}`);
        }
    })
});