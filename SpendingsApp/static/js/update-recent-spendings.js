
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
                const date = new Date(spending.spendingDate);
                const date_text = $.format.date(date, "dd.MM.yyyy")
                
                const buttonClasses = "btn btn-sm py-0 px-1";
                const editLink = `spending/edit/${spending.id}`;
                const editButton = `<a href='${editLink}' class='${buttonClasses} btn-outline-secondary'><i class='bi bi-pencil'></i></a>`;

                const deleteIcon = "<i class='bi bi-trash'></i>"
                const deleteButtonClasses = `${buttonClasses} btn-outline-danger delete-spending-btn`;
                const deleteButton = `<button class='${deleteButtonClasses}' data-spending-id='${spending.id}'>${deleteIcon}</button>`;

                const date_cell = `<td class='text-nowrap text-truncate'>${date_text}</td>`;
                const category_cell = `<td class='text-nowrap text-truncate'>${spending.category.name}</td>`;
                const description_cell = `<td class='text-nowrap text-truncate'>${spending.description}</td>`;
                const amount_cell = `<td class='text-end'>${spending.amount}</td>`;
                const edit_cell = `<td class='text-end'>${editButton}</td>`;
                const delete_cell = `<td class='text-end'>${deleteButton}</td>`;

                const row = `<tr>${date_cell}${category_cell}${description_cell}${amount_cell}${edit_cell}${delete_cell}</tr>`;
                $('#table-spendings tbody').append(row);
            });
        }
    })
}

$(document).ready(function() {
    updateRecentSpendings();
});
