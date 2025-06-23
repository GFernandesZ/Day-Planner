document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('id_password1');
    const confirmPasswordInput = document.getElementById('id_password2');
    const usernameInput = document.getElementById('id_username');
    const emailInput = document.getElementById('id_email');

    const togglePassword = document.getElementById('togglePassword');
    const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');

    const eyeIcon = document.getElementById('eyeIcon');
    const eyeOffIcon = document.getElementById('eyeOffIcon');
    const confirmEyeIcon = document.getElementById('confirmEyeIcon');
    const confirmEyeOffIcon = document.getElementById('confirmEyeOffIcon');

    // Adicionar classe input-field aos campos
    if (passwordInput) passwordInput.classList.add('input-field');
    if (confirmPasswordInput) confirmPasswordInput.classList.add('input-field');
    if (usernameInput) usernameInput.classList.add('input-field');
    if (emailInput) emailInput.classList.add('input-field');

    function toggleVisibility(inputElement, eyeOpenIcon, eyeClosedIcon) {
        const type = inputElement.getAttribute('type') === 'password' ? 'text' : 'password';
        inputElement.setAttribute('type', type);
        eyeOpenIcon.classList.toggle('hidden');
        eyeClosedIcon.classList.toggle('hidden');
    }

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function () {
            toggleVisibility(passwordInput, eyeIcon, eyeOffIcon);
        });
    }

    if (toggleConfirmPassword && confirmPasswordInput) {
        toggleConfirmPassword.addEventListener('click', function () {
            toggleVisibility(confirmPasswordInput, confirmEyeIcon, confirmEyeOffIcon);
        });
    }
});
