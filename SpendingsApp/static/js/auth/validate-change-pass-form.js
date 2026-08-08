
const CHANGE_PASSWORD_FORM_RULES = {
    "old-password": {
        required: true
    },
    "new-password1": {
        required: true,
        minlength: 8
    },
    "new-password2": {
        required: true,
        equalTo: "#new-password1"
    }
};

const CHANGE_PASSWORD_FORM_MESSAGES = {
    "old-password": "Please enter your current password",
    "new-password1": "Please enter a new password (min 8 characters)",
    "new-password2": "Passwords do not match"
};

export function validateChangePasswordForm(formId) {
    const form = $(formId);
    if (typeof form.validate !== 'function') {
        console.warn('jQuery Validate plugin not found — client-side validation disabled for', formId);
        return;
    }
    form.validate({
        rules: CHANGE_PASSWORD_FORM_RULES,
        messages: CHANGE_PASSWORD_FORM_MESSAGES
    });
}