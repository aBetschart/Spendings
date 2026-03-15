
import { renderSpendingsTbody } from './render-spendings-tbody.js';

export function updateRecentSpendings() {
    $.ajax({
        type: "POST",
        datatype: "json",
        contenttype: "application/json",
        data: {spendings_count: 10, csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
        url: DJANGO_URLS.spending_get_recent,
        success: function(data) {
            const spendings = data.spendings || [];
            const table = document.getElementById('table-spendings');
            if (!table) 
                return;
            
            const oldTbody = table.querySelector('tbody');
            const newTbody = renderSpendingsTbody(spendings);
            if (oldTbody) {
                newTbody.className = oldTbody.className;
                oldTbody.replaceWith(newTbody);
            } else {
                table.appendChild(newTbody);
            }
        }
    })
}

$(document).ready(function() {
    updateRecentSpendings();
});
