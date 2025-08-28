
function validarCorreo() {
    const email = document.getElementById("email").value;
    const confirmEmail = document.getElementById("confirm_email").value;

    if (email !== confirmEmail) {
        alert("Los correos electrónicos no coinciden.");
        return false; // Bloquea el envío del formulario
    }
    return true; // Permite el envío
}