/* ==========================================================
   PhishGuard - Custom JavaScript
   ========================================================== */

document.addEventListener("DOMContentLoaded", function () {

    // ----------------------------------------------------
    // Auto-dismiss flash messages after 5 seconds
    // ----------------------------------------------------
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });

    // ----------------------------------------------------
    // Client-side password match validation on Register page
    // ----------------------------------------------------
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        registerForm.addEventListener("submit", function (e) {
            const password = document.getElementById("password");
            const confirmPassword = document.getElementById("confirm_password");
            if (password && confirmPassword && password.value !== confirmPassword.value) {
                e.preventDefault();
                alert("Passwords do not match. Please check and try again.");
            }
        });
    }

    // ----------------------------------------------------
    // Prevent submitting an empty email on the Detect page
    // ----------------------------------------------------
    const detectForm = document.getElementById("detectForm");
    if (detectForm) {
        detectForm.addEventListener("submit", function (e) {
            const emailText = document.getElementById("email_text");
            if (emailText && emailText.value.trim().length === 0) {
                e.preventDefault();
                alert("Please enter some email content before analyzing.");
            }
        });
    }

});
