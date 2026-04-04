
import { MonthlyAccordionRenderer } from "./monthly-accordion-renderer.js";

export class CategoryReport {
    constructor(categoryName, monthlyTotals, yearlyTotal) {
        this.categoryName = categoryName;
        this.monthlyTotals = monthlyTotals;
        this.yearlyTotal = yearlyTotal
    }
}

export class YearlyOverviewTableRenderer {
    constructor() {
        this.accordionRenderer = new MonthlyAccordionRenderer();
    }

    
    render(categoryReports) {
        const table = document.createElement('table');
        table.classList.add('table', 'table-hover');
        const thead = this.#renderTableHeader();
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        tbody.classList.add('table-group-divider');
        table.appendChild(tbody);

        categoryReports.forEach((report, index) => {
            const accordion = this.accordionRenderer.render(index, report.categoryName, report.monthlyTotals);

            const yearlyTotal = parseFloat(report.yearlyTotal)
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="text-start">
                    ${accordion.outerHTML}
                </td>
                <td class="text-end">
                    ${yearlyTotal.toFixed(2)}
                </td>`;
            tbody.appendChild(row);
        });

        return table;
    }

    #renderTableHeader() {
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr class="text-start">
                <th></th>
                <th class="text-end">Total</th>
            </tr>`;
        return thead;
    }
}