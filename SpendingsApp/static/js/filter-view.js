
import { validateFilterForm } from "./filter-form-validate.js";
import { renderSpendingsTbody } from "./render-spendings-tbody.js";

$(document).ready(function() {
    prepareFilterForm();
    updateSpendings();
    
    const form = document.getElementById('filter-form');
    form.addEventListener('change', updateSpendings);
});

function prepareFilterForm() {
    const today = new Date();
    const startDate = dateFns.startOfMonth(today);
    const endDate = today;

    const startDateInput = document.getElementById('id_start_date');
    const endDateInput = document.getElementById('id_end_date');

    startDateInput.value = dateFns.format(startDate, "yyyy-MM-dd");
    endDateInput.value = dateFns.format(endDate, "yyyy-MM-dd");
};

async function updateSpendings() {
    console.log("change");

    validateFilterForm("#filter-form");

    const spendings = await fetchSpendings();
    const spendingsCount = spendings.length;
    console.log(`Fetched ${spendingsCount} spendings`);

    const tbody = renderSpendingsTbody(spendings);
    tbody.id = 'spendings-table-body';
    const tableBody = document.getElementById('spendings-table-body');
    tableBody.replaceWith(tbody);
};

async function fetchSpendings() {
    const startDate = document.getElementById('id_start_date').value;
    const endDate = document.getElementById('id_end_date').value;

    const isoStartDate = dateFns.format(new Date(startDate), 'yyyy-MM-dd');
    const isoEndDate = dateFns.format(new Date(endDate), 'yyyy-MM-dd');
    
    const filterData = {
        start_date: isoStartDate,
        end_date: isoEndDate    
    };
    
    const categorySelect = document.getElementById('id_categories');
    const categoryIds = Array.from(categorySelect.selectedOptions).map(option => option.value);

    if (categoryIds.length > 0)
        filterData.categories = categoryIds;


    console.log("Fetching spendings with filter:", filterData);


    try {
        const data = await $.ajax({
            type: "GET",
            url: DJANGO_URLS.spending_get,
            dataType: "json",
            data: filterData,
            traditional: true
        });
        return data.spendings;

    } catch (xhr) {
        console.error("Error status:", xhr.status);
        console.error("Error response:", xhr.responseText);
        alert("Error loading spendings. Check console.");
        throw xhr;
    }
}