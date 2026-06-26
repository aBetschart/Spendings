
const CHANGE_PASSWORD_FORM_RULES = {
    "username": {
        required: true
    },
    "email": {
        required: true,
        minlength: 8
    },
    "password1": {
        required: true,
        minlength: 8
    },
    "password2": {
        required: true,
        equalTo: "#password1"
    }
};

const CHANGE_PASSWORD_FORM_MESSAGES = {
    "username": "Please enter your username",
    "email": "Please enter a valid email address",
    "password1": "Please enter a password (min 8 characters)",
    "password2": "Passwords do not match"
};

export function validateRegisterForm(formId) {
    const form = $(formId);
    if (form.length === 0) {
        console.warn('Form not found for validation:', formId);
        return;
    }

    if (typeof form.validate !== 'function') {
        console.warn('jQuery Validate plugin not found — client-side validation disabled for', formId);
        return;
    }
    form.validate({
        rules: CHANGE_PASSWORD_FORM_RULES,
        messages: CHANGE_PASSWORD_FORM_MESSAGES
    });
}