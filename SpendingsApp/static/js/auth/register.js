
import { validateRegisterForm } from "./validate-register-form.js";
import { showMessageBox } from '../messaging/show-message-box.js';

const REGISTER_FORM_ID = "#register-form";

const USERNAME_FIELD_ID = "#username";
const EMAIL_FIELD_ID = "#email";
const PASSWORD1_FIELD_ID = "#password1";
const PASSWORD2_FIELD_ID = "#password2";

$(document).ready(function() {
    validateRegisterForm(REGISTER_FORM_ID);

    $(REGISTER_FORM_ID).on("submit", function(event) {
        event.preventDefault();

        validateRegisterForm(REGISTER_FORM_ID);
        const form = $(this);
        if (!form.valid()) {
            return;
        }

        const formData = {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            username: $(USERNAME_FIELD_ID).val(),
            email: $(EMAIL_FIELD_ID).val(),
            password: $(PASSWORD1_FIELD_ID).val()
        };
        $.ajax({
            url: DJANGO_URLS.user_add,
            type: "POST",
            data: formData,
            success: function(response) {
                showMessageBox("Registration successful!", "success");
            },
            error: function(xhr, status, error) {
                const message = 'Error registering user: ' + '<br>' + xhr.responseText;
                showMessageBox(message, "error");
            }
        });
    });
});