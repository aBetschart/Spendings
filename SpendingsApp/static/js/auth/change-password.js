import { validateChangePasswordForm } from './validate-change-pass-form.js';
import { showMessageBox } from '../messaging/show-message-box.js';


const CHANGE_PASSWORD_URL = DJANGO_URLS.change_password;

const CHANGE_PASSWORD_BUTTON_ID = "#change-password-button";
const CHANGE_PASSWORD_FORM_ID = "#change-password-form";

const ID_OLD_PASSWORD = "#old-password";
const ID_NEW_PASSWORD1 = "#new-password1";
const ID_NEW_PASSWORD2 = "#new-password2";

$(document).ready(function() {

    validateChangePasswordForm(CHANGE_PASSWORD_FORM_ID);

    $(CHANGE_PASSWORD_BUTTON_ID).click(function(event) {
        event.preventDefault();
        validateChangePasswordForm(CHANGE_PASSWORD_FORM_ID);
        const $form = $(CHANGE_PASSWORD_FORM_ID);
        if (typeof $form.valid === 'function' && !$form.valid()) 
            return;

        const oldPassword = $(ID_OLD_PASSWORD).val();
        const newPassword1 = $(ID_NEW_PASSWORD1).val();
        const newPassword2 = $(ID_NEW_PASSWORD2).val();
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: CHANGE_PASSWORD_URL,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrfToken,
                OldPassword: oldPassword,
                NewPassword: newPassword1,
            },
            success: function(response) {
                showMessageBox('Password changed successfully.', 'success');
            },
            error: function(xhr, status, error) {
                const message = 'Error changing password: ' + '<br>' + xhr.responseText;
                console.error(message);
                showMessageBox('#password-toast', message, 'error');
            }
        })
    })
    


});