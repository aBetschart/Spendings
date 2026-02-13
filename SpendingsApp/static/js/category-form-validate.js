const CATEGORY_MIN_LENGTH = 3;
const CATEGORY_MAX_LENGTH = 50;

const CATEGORY_VALIDATE_RULES = {
    "name": {
        required: true,
        minlength: CATEGORY_MIN_LENGTH,
        maxlength: CATEGORY_MAX_LENGTH
    }
};

const CATEGORY_FORM_MESSAGES = {
    "name": {
        required: `Please enter a category name`,
        minlength: `Category name must be at least ${CATEGORY_MIN_LENGTH} characters long`,
        maxlength: `Category name must be at most ${CATEGORY_MAX_LENGTH} characters long`
    }
};

export function validateCategoryForm(formId) {
    // guard if jQuery Validate isn't available (prevents uncaught exception)
    if (typeof $(formId).validate !== 'function') {
        console.warn('jQuery Validate plugin not found — client-side validation disabled for', formId);
        return;
    }

    $(formId).validate({
        rules: CATEGORY_VALIDATE_RULES,
        messages: CATEGORY_FORM_MESSAGES
    });
}