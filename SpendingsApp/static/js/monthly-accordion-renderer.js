
class MonthlyAccordionRenderer {

    render(index, categoryName, monthlyTotals) {
        const accordion = this.#renderBaseAccordion(index, categoryName);
        const totalsTable = this.#renderTotalsTable(monthlyTotals);
        accordion.querySelector('.accordion-body').appendChild(totalsTable);
        return accordion;
    }

    #renderBaseAccordion(index, categoryName) {
        const accordionDiv = document.createElement('div');
        accordionDiv.classList.add('accordion');
        accordionDiv.id = `accordion-${index}`;

        const accordionItemDiv = document.createElement('div');
        accordionItemDiv.classList.add('accordion-item');
        accordionDiv.appendChild(accordionItemDiv);

        const accordionHeader = document.createElement('h2');
        accordionHeader.classList.add('accordion-header');
        accordionItemDiv.appendChild(accordionHeader);
        
        const accordionButton = document.createElement('button');
        accordionButton.classList.add('accordion-button', 'collapsed');
        accordionButton.type = 'button';
        accordionButton.setAttribute('data-bs-toggle', 'collapse');
        accordionButton.setAttribute('data-bs-target', `#collapse-${index}`);
        accordionButton.setAttribute('aria-expanded', 'false');
        accordionButton.setAttribute('aria-controls', `collapse-${index}`);
        accordionButton.textContent = categoryName;
        accordionHeader.appendChild(accordionButton);

        const collapseDiv = document.createElement('div');
        collapseDiv.id = `collapse-${index}`;
        collapseDiv.classList.add('accordion-collapse', 'collapse');
        collapseDiv.setAttribute('aria-labelledby', `heading-${index}`);
        collapseDiv.setAttribute('data-bs-parent', `#accordion-${index}`);
        accordionItemDiv.appendChild(collapseDiv);

        const accordionBody = document.createElement('div');
        accordionBody.classList.add('accordion-body');
        collapseDiv.appendChild(accordionBody);

        return accordionDiv;
    }

    #renderTotalsTable(monthlyTotals) {
        if (monthlyTotals.length != 12) 
            throw new Error("Expected 12 monthly totals, got " + monthlyTotals.length);

        const table = document.createElement('table');
        table.classList.add('table');
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        headerRow.classList.add('text-end');
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        months.forEach(month => {
            const th = document.createElement('th');
            th.classList.add('col-1');
            th.textContent = month;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        const dataRow = document.createElement('tr');
        dataRow.classList.add('text-end');
        
        monthlyTotals.forEach(total => {
            const td = document.createElement('td');
            td.textContent = total.toFixed(2);
            dataRow.appendChild(td);
        });
        tbody.appendChild(dataRow);
        table.appendChild(tbody);
    }
}