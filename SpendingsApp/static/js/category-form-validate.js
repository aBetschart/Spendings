const CATEGORY_MIN_LENGTH = 3;
const CATEGORY_MAX_LENGTH = 50;

const CATEGORY_VALIDATE_RULES = {
    "name": {
        required: true,
        minLength: CATEGORY_MIN_LENGTH,
        maxLength: CATEGORY_MAX_LENGTH
    }
};

const SPENDING_FORM_MESSAGES = {
    "name": {
        required: `Please enter a category name`,
        minLength: `Category name must be at least ${CATEGORY_MIN_LENGTH} characters long`,
        maxLength: `Category name must be at most ${CATEGORY_MAX_LENGTH} characters long`
    }
};

export function validateCategoryForm(formId) {
    $(formId).validate({
        rules: CATEGORY_VALIDATE_RULES,
        messages: SPENDING_FORM_MESSAGES
    });
}