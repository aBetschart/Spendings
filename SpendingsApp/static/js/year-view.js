
import { YearlyOverviewTableRenderer } from "./yearly-overview-table-renderer.js";
import { CategoryReport } from "./yearly-overview-table-renderer.js";
import { validateYearForm } from "./year-form-validation.js";

$(document).ready(function () {
    validateYearForm("#year-form");

    const yearForm = document.getElementById('year-form');
    yearForm.addEventListener('change', updateYearlyOverview);

    updateYearlyOverview()
});


async function updateYearlyOverview() {
    if (!$("#year-form").valid())
        return;

    clearYearlyOverview();
    showLoader();

    try {
        await renderYearlyOverview();    
    }
    catch (error) {
        console.error("Error rendering yearly overview:", error);
        renderError();
    }
    finally {
        hideLoader();
    }
}

function showLoader() {
    const loader = document.getElementById("loader");
    if (loader != null)
        loader.classList.remove("d-none");
}

function hideLoader() {
    const loader = document.getElementById("loader");
    if (loader != null)
        loader.classList.add("d-none");
}

function clearYearlyOverview() {
    const container = document.getElementById('yearly-overview-container');
    container.innerHTML = '';
}

async function renderYearlyOverview() {
    const year = getYearFromForm();
    const categories = await getCategories();
    const categoryReports = await composeCategoryReports(year, categories);
    const yearlyTotal = categoryReports.reduce((sum, report) => sum + report.yearlyTotal, 0);
    
    const renderer = new YearlyOverviewTableRenderer();
    const table = renderer.render(categoryReports, yearlyTotal);
    
    const container = document.getElementById('yearly-overview-container');
    container.innerHTML = '';
    container.appendChild(table);
}

function getYearFromForm() {
    const yearInput = document.getElementById('id_year');
    return parseInt(yearInput.value);
}

async function getCategories() {
    try {
        const data = await $.ajax({
            type: "GET",
            url: DJANGO_URLS.category_get,
        });
        return data.categories;
    }
    catch (error) {
        console.error("Error fetching categories:", error);
        throw new Error("Failed to fetch categories");
    }
}

async function composeCategoryReports(year, categories) {
    return await Promise.all(categories.map(category => composeCategoryReport(year, category)));
}

async function composeCategoryReport(year, category) {
    const monthlyTotals = await Promise.all(
        Array.from({length: 12}, (_, month) => fetchMonthlyTotal(year, month, category))
    );
    const yearlyTotal = monthlyTotals.reduce((sum, total) => sum + total, 0);
    return new CategoryReport(category.name, monthlyTotals, yearlyTotal);
}

async function fetchMonthlyTotal(year, month, category) {
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const isoFirstDay = dateFns.format(firstDay, 'yyyy-MM-dd');
    const isoLastDay = dateFns.format(lastDay, 'yyyy-MM-dd');
    const categories = [category.id];
    const data = await $.ajax({
            type: "GET",
            url: DJANGO_URLS.spending_get,
            dataType: "json",
            traditional: true,
            data: {
                categories: categories,
                start_date: isoFirstDay,
                end_date: isoLastDay
            }});
    return parseFloat(data.total);
}

function renderError() {
    const message = "Ooops, something went wrong while loading the yearly overview. Check log for details.";
    const errorDiv = document.createElement('div');
    errorDiv.classList.add('alert', 'alert-danger', 'd-flex', 'align-items-start', 'gap-3', 'p-4', 'rounded-4', 'shadow-sm');
    errorDiv.setAttribute('role', 'alert');
    errorDiv.innerHTML = `
        <i class="bi bi-x-octagon-fill fs-1"></i>
        <div id="error-box">
            <h4 class="alert-heading mb-2">Ooops! Something broke</h4>
            <p class="mb-3">${message}</p>
        </div>
    `;
    const container = document.getElementById('yearly-overview-container');
    container.innerHTML = '';
    container.appendChild(errorDiv);
}
