const YEAR_FORM_RULES = {
    year: {
        required: true,
        number: true,
        min: 1900,
        max: 2100
    }
};

const YEAR_FORM_MESSAGES = {
    year: "Please enter a valid year (between 1900 and 2100)"
};

export function validateYearForm(formId) {
    $(formId).validate({
        rules: YEAR_FORM_RULES,
        messages: YEAR_FORM_MESSAGES
    });
}