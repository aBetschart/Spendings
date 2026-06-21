
CHANGE_PASSWORD_FORM_RULES = {
    oldPassword: {
        required: true,
        minlength: 8
    },
    newPassword1: {
        required: true,
        minlength: 8
    },
    newPassword2: {
        required: true,
        equalTo: "#id_new_password1"
    }
};

CHANGE_PASSWORD_FORM_MESSAGES = {
    oldPassword: "Please enter your current password (min 8 characters)",
    newPassword1: "Please enter a new password (min 8 characters)",
    newPassword2: "Passwords do not match"
};

function validateChangePasswordForm(formId) {
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