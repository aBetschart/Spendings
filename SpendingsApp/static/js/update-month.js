import { renderSpendingsTbody } from './render-spendings-tbody.js';

(function(){
    function renderMonthTable(spendings){
        const table = document.getElementById('month-spendings-table');
        const tbody = document.getElementById('month-spendings-tbody');
        if(!tbody || !table) return;

        if (table.querySelector('tfoot')) table.querySelector('tfoot').remove();

        if(!spendings || spendings.length === 0){
            const tr = document.createElement('tr');
            const td = document.createElement('td');

            const iElment = document.createElement('i');
            iElment.className = 'bi bi-emoji-frown-fill';

            td.colSpan = 6;
            td.textContent = 'No entries found ';
            td.appendChild(iElment);
            
            tr.appendChild(td);

            tbody.innerHTML = '';
            tbody.appendChild(tr);
            
            return;
        }

        const newTbody = renderSpendingsTbody(spendings);
        newTbody.id = tbody.id;
        newTbody.className = tbody.className;
        tbody.replaceWith(newTbody);

        
        const tfoot = document.createElement('tfoot');
        tfoot.className = 'table-group-divider';

        const totalTr = document.createElement('tr');
        
        const totalLabelTd = document.createElement('td');
        totalLabelTd.className = 'text-end';
        totalLabelTd.textContent = 'Total';
        totalLabelTd.colSpan = 3;
        
        const totalAmountTd = document.createElement('td');
        totalAmountTd.className = 'text-end';
        const totalAmount = extract_total(spendings);
        totalAmountTd.textContent = totalAmount.toFixed(2);
        
        const backTd = document.createElement('td');
        backTd.colSpan = 2;

        totalTr.appendChild(totalLabelTd);
        totalTr.appendChild(totalAmountTd);
        totalTr.appendChild(backTd);
        
        tfoot.appendChild(totalTr);

        table.appendChild(tfoot);
    }

    function extract_total(spendings) {
        return spendings.reduce(function(acc, spending) {
            return acc + Number(spending.amount);
        }, 0);
    }

    function fetchSpendingsForMonth(monthName, year){
        const monthLabel = String(monthName).toLowerCase();
        const monthLabelCap = monthLabel.charAt(0).toUpperCase() + monthLabel.slice(1);

        const parsed = dateFns.parse(`${monthLabelCap} ${year}`, 'MMMM yyyy', new Date());
        if (!dateFns.isValid(parsed)) {
            console.error('Invalid month/year', monthName, year);
            return;
        }

        const start = dateFns.startOfMonth(parsed);
        const end = dateFns.endOfMonth(parsed);
        const startIso = dateFns.format(start, 'yyyy-MM-dd');
        const endIso = dateFns.format(end, 'yyyy-MM-dd');

        $.ajax({
            type: 'GET',
            url: DJANGO_URLS.spending_get,
            data: { start_date: startIso, end_date: endIso },
            success: function(data){
                renderMonthTable(data.spendings);
            },
            error: function(xhr){
                console.error('Error fetching month spendings', xhr.status, xhr.responseText);
            }
        });
    }

    function wireMonthForm(){
        const form = document.getElementById('month-form');
        if(!form) return;
        form.addEventListener('submit', function(ev){
            ev.preventDefault();
            const monthField = form.querySelector('[name="month"]');
            const yearField = form.querySelector('[name="year"]');
            if(!monthField || !yearField) return;
            fetchSpendingsForMonth(monthField.value, yearField.value);
        });

        const monthField = form.querySelector('[name="month"]');
        const yearField = form.querySelector('[name="year"]');
        if(monthField && yearField) {
            fetchSpendingsForMonth(monthField.value, yearField.value);
        }
    }

    document.addEventListener('DOMContentLoaded', wireMonthForm);
    window.fetchSpendingsForMonth = fetchSpendingsForMonth;
})();
