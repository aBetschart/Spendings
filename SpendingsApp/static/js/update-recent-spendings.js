
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

$(document).ready(function() {
    updateRecentSpendings();
});
