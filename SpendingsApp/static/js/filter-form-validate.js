

const VALIDATION_RULES = {
    "start_date": {
        required: true,
        date: true
    },
    "end_date": {
        required: true,
        date: true
    },
    "description": {
        required: false,
        minlength: 3,
        maxlength: 100
    },
    "min_amount": {
        required: false,
        number: true,
        min: 0
    },
    "max_amount": {
        required: false,
        number: true,
        min: 0.01
    },
    "categories": {
        required: false
    }
};

const VALIDATION_MESSAGES = {
    "start_date": {
        required: "Please enter a start date",
        date: "Please enter a valid date"
    },
    "end_date": {
        required: "Please enter an end date",
        date: "Please enter a valid date"
    },
    "description": {
        minlength: "Description must be at least 3 characters long",
        maxlength: "Description must be at most 100 characters long"
    },
    "min_amount": {
        number: "Please enter a valid number",
        min: "Minimum amount cannot be negative"
    },
    "max_amount": {
        number: "Please enter a valid number",
        min: "Maximum amount must be greater or equal to 0.01"
    },
};

export function validateFilterForm(formId) {
    if (typeof $(formId).validate !== 'function') {
        console.warn('jQuery Validate plugin not found — client-side validation disabled for', formId);
        return;
    }

    $(formId).validate({
        rules: VALIDATION_RULES,
        messages: VALIDATION_MESSAGES
    });
}