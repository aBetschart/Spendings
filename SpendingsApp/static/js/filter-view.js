
import { validateFilterForm } from "./filter-form-validate.js";

$(document).ready(function() {
    const today = new Date();
    const firstDayOfMonth = dateFns.startOfMonth(today);
    const lastDayOfMonth = dateFns.endOfMonth(today);

    const first_day_val = dateFns.format(firstDayOfMonth, "yyyy-MM-dd");
    const startDateInput = document.getElementById('id_start_date');
    startDateInput.value = first_day_val;

    const lastDayVal = dateFns.format(lastDayOfMonth, "yyyy-MM-dd");
    const endDateInput = document.getElementById('id_end_date');
    endDateInput.value = lastDayVal;

    
    
    const form = document.getElementById('filter-form');
    form.addEventListener('change', updateSpendings);
});

function updateSpendings() {
    console.log("change");

    validateFilterForm("#filter-form");

    // $.ajax({
    //     type: "GET",
    //     url: DJANGO_URLS.spending_get,
    //     dataType: "json",

    // });
};