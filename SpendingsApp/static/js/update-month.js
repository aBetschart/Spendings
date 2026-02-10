(function(){
    function renderMonthTable(spendings){
        const tbody = document.getElementById('month-spendings-tbody');
        if(!tbody) return;
        tbody.innerHTML = '';

        if(!spendings || spendings.length === 0){
            const tr = document.createElement('tr');
            const td = document.createElement('td');

            const iElment = document.createElement('i');
            iElment.className = 'bi bi-emoji-frown-fill';

            td.colSpan = 4;
            td.textContent = 'No entries found ';
            td.appendChild(iElment);
            
            tr.appendChild(td);
            
            tbody.appendChild(tr);
            
            return;
        }

        spendings.forEach(function(spending) {
            const tr = document.createElement('tr');

            const dateTd = document.createElement('td');
            const d = new Date(spending.spendingDate);
            dateTd.textContent = d.toLocaleDateString();

            const categoryTd = document.createElement('td');
            categoryTd.textContent = spending.category.name;

            const descriptionTd = document.createElement('td');
            descriptionTd.textContent = spending.description;

            const amountTd = document.createElement('td');
            amountTd.className = 'text-end';
            const a = document.createElement('a');
            a.className = 'link-underline link-underline-opacity-0';
            a.href = 'spending/edit/' + spending.id;
            a.textContent = Number(spending.amount).toFixed(2);
            amountTd.appendChild(a);

            tr.appendChild(dateTd);
            tr.appendChild(categoryTd);
            tr.appendChild(descriptionTd);
            tr.appendChild(amountTd);

            tbody.appendChild(tr);
        });

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
        
        totalTr.appendChild(totalLabelTd);
        totalTr.appendChild(totalAmountTd);
        tfoot.appendChild(totalTr);

        table = document.getElementById('month-spendings-table');
        if (table) 
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

    // expose helper for other modules if needed
    window.fetchSpendingsForMonth = fetchSpendingsForMonth;
})();
