

export function renderSpendingsTbody(spendings) {
    const tbody = document.createElement('tbody');

    spendings.forEach(spending => {
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
        amountTd.textContent = Number(spending.amount).toFixed(2);

        const buttonClasses = "btn btn-sm py-0 px-1";
        
        const editButton = document.createElement('a');
        editButton.href = `/spending/edit/${spending.id}`;
        editButton.className = `${buttonClasses} btn-outline-secondary`;
        const editIcon = document.createElement('i');
        editIcon.className = 'bi bi-pencil';
        editButton.appendChild(editIcon);
        
        const deleteButton = document.createElement('button');
        deleteButton.className = `${buttonClasses} btn-outline-danger delete-spending-btn`;
        deleteButton.dataset.spendingId = spending.id;
        
        const deleteIcon = document.createElement('i');
        deleteIcon.className = 'bi bi-trash';
        
        const editTd = document.createElement('td');
        editTd.appendChild(editButton);

        deleteButton.appendChild(deleteIcon);
        const deleteTd = document.createElement('td');
        deleteTd.appendChild(deleteButton);

        tr.appendChild(dateTd);
        tr.appendChild(categoryTd);
        tr.appendChild(descriptionTd);
        tr.appendChild(amountTd);
        tr.appendChild(editTd);
        tr.appendChild(deleteTd);

        tbody.appendChild(tr);
    });

    return tbody;
}