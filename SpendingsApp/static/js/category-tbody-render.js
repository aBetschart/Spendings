

export function renderCategoriesTbody(categories) {
    const tbody = document.createElement('tbody');

    categories.forEach(category => {
        const tr = document.createElement('tr');

        const nameTd = document.createElement('td');
        nameTd.textContent = category.name;
        nameTd.style.width = "90%";

        const buttonClasses = "btn btn-sm py-0 px-1";

        const editButton = document.createElement('a');
        editButton.href = `categories/edit/${category.id}`;
        editButton.className = `${buttonClasses} btn-outline-secondary`;
        const editIcon = document.createElement('i');
        editIcon.className = 'bi bi-pencil';
        editButton.appendChild(editIcon);
        const editTd = document.createElement('td');
        editTd.style.width = "5%";
        editTd.appendChild(editButton);

        const deleteButton = document.createElement('button');
        deleteButton.className = `${buttonClasses} btn-outline-danger delete-category-btn`;
        deleteButton.dataset.categoryId = category.id;
        const deleteIcon = document.createElement('i');
        deleteIcon.className = 'bi bi-trash';
        deleteButton.appendChild(deleteIcon);
        const deleteTd = document.createElement('td');
        deleteTd.style.width = "5%";
        deleteTd.appendChild(deleteButton);

        tr.appendChild(nameTd);
        tr.appendChild(editTd);
        tr.appendChild(deleteTd);
        tbody.appendChild(tr);
    });

    return tbody;
}
