import { validatePasswordForm } from './validate-change-pass-form.js';

// TODO: Implement the change password functionality using AJAX and handle the response accordingly.

const CHANGE_PASSWORD_URL = "";

const CHANGE_PASSWORD_BUTTON_ID = "#change-password-button";
const CHANGE_PASSWORD_FORM_ID = "#change-password-form";

const ID_OLD_PASSWORD = "#old-password";
const ID_NEW_PASSWORD1 = "#new-password1";
const ID_NEW_PASSWORD2 = "#new-password2";

$(document).ready(function() {

    validatePasswordForm(CHANGE_PASSWORD_FORM_ID);

    $(CHANGE_PASSWORD_BUTTON_ID).click(function(event) {
        event.preventDefault();
        validatePasswordForm(CHANGE_PASSWORD_FORM_ID);
        const $form = $(CHANGE_PASSWORD_FORM_ID);
        if (typeof $form.valid === 'function' && !$form.valid()) 
            return;

        const oldPassword = $(ID_OLD_PASSWORD).val();
        const newPassword1 = $(ID_NEW_PASSWORD1).val();
        const newPassword2 = $(ID_NEW_PASSWORD2).val();
    })
    


});