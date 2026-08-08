

const COLOR_CLASSES = {
    'info': 'text-bg-primary',
    'success': 'text-bg-success',
    'warning': 'text-bg-warning',
    'error': 'text-bg-danger'
};

export function showMessageBox(message, type = 'info') {
    const colorClass = COLOR_CLASSES[type] || 'text-bg-primary';
    const toastDiv = generateToastDiv(message, colorClass);

    const container = getContainer();
    container.appendChild(toastDiv);
    
    const toast = new bootstrap.Toast(toastDiv);
    toast.show();
}

function generateToastDiv(message, colorClass) {
    const toastDiv = document.createElement('div');
    toastDiv.classList.add('toast', 'align-items-center', colorClass, 'border-0');
    toastDiv.setAttribute('role', 'alert');
    toastDiv.setAttribute('aria-live', 'assertive');
    toastDiv.setAttribute('aria-atomic', 'true');
    const closeButton = '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>'
    toastDiv.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>         
            ${closeButton}
        </div>
    `;
    return toastDiv;
}

function getContainer() {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.classList.add('toast-container', 'position-fixed', 'bottom-0', 'start-0', 'p-3');
        document.body.appendChild(container);
    }
    return container;
}