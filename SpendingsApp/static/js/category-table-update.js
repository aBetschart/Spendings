import { renderCategoriesTbody } from './category-tbody-render.js';


export function categoryTableUpdate() {
    $.ajax({
        type: "GET",
        url: DJANGO_URLS.category_get,
        success: function(data) {
            const categoryTable = document.getElementById('category-table');
            if (!categoryTable || !data.categories)
                return;
            
            const newTbody = renderCategoriesTbody(data.categories);
            const oldTbody = categoryTable.querySelector('tbody');
            if (oldTbody)
                categoryTable.replaceChild(newTbody, oldTbody);
            else
                categoryTable.appendChild(newTbody);
        },
        error(xhr, _status, error) {
            console.error("Error status:", xhr.status);
            console.error("Error response:", xhr.responseText);
            console.error("Error message:", error);
            alert("Error updating category table. Please check the console.");
        }
    });

}