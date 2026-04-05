
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

    render(categoryReports, yearlyTotal) {
        const table = document.createElement('table');
        table.classList.add('table', 'table-hover');

        const thead = this.#renderTableHeader();
        table.appendChild(thead);

        const tbody = this.#renderTableBody(categoryReports);
        table.appendChild(tbody);

        const tfoot = this.#renderTableFooter(yearlyTotal);
        table.appendChild(tfoot);
        
        return table;
    }
    
    #renderTableHeader() {
        const thead = document.createElement('thead');
        thead.innerHTML = `
                <tr class="text-end">
                    <th class="col-10"></th>
                    <th class="col-1">Avg.</th>
                    <th class="col-1">Total</th>
                </tr>
            `;
        return thead;
    }
    
    #renderTableBody(categoryReports) {
        const tbody = document.createElement('tbody');
        tbody.classList.add('table-group-divider');

        categoryReports.forEach((report, index) => {
            const accordion = this.accordionRenderer.render(index, report.categoryName, report.monthlyTotals);

            const yearlyTotal = parseFloat(report.yearlyTotal);
            const row = document.createElement('tr');
            row.innerHTML = `
                    <td class="text-start">
                        ${accordion.outerHTML}
                    </td>
                    <td class="text-end">
                        0.00
                    </td>
                    <td class="text-end">
                        ${yearlyTotal.toFixed(2)}
                    </td>
                `;

            tbody.appendChild(row);
        });
        return tbody;
    }

    #renderTableFooter(yearlyTotal) {
        const tfoot = document.createElement('tfoot');
        tfoot.classList.add('table-group-divider');
        const totalString = yearlyTotal.toLocaleString('de-CH', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        tfoot.innerHTML = `
                <tr>
                    <td colspan="2" class="text-end"></td>
                    <td class="text-end"><strong>${totalString}</strong></td>
                </tr>
            `;
        return tfoot;
    }
}