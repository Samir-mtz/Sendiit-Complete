const inputs = document.querySelectorAll("#formulario input");
const form = document.getElementById("formulario");
const nombre = document.getElementById("nombre");
const email = document.getElementById("email");
const password = document.getElementById("password");
const password2 = document.getElementById("password_confirm");
const telefono = document.getElementById("telefono");
const direccion = document.getElementById("direccion");

form.addEventListener("submit", (e) => {
	e.preventDefault();
	checkInputs();
});

inputs.forEach((input) => {
	input.addEventListener("keyup", checkInputs);
	input.addEventListener("blur", checkInputs);
});

function checkInputs() {
	const nombreValue = nombre.value.trim();
	const emailValue = email.value.trim();
	const passwordValue = password.value.trim();
	const password2Value = password2.value.trim();
	const telefonoValue = telefono.value.trim();
	const direccionValue = direccion.value.trim();

	// Comparacion del nombre
	if (nombreValue === "") {
		setErrorFor(nombre, "No puede dejar el nombre en blanco.");
	} else if (!comprobarNombre(nombreValue)) {
		setErrorFor(nombre, "El nombre solo puede tener letras mayusculas, minusculas y espacios.");
	} else {
		setSuccessFor(nombre);
	}

	// Comparacion del email
	if (emailValue === "") {
		setErrorFor(email, "No puede dejar el email en blanco.");
	} else if (!comprobarEmail(emailValue)) {
		setErrorFor(email, "No ingreso un un formato de email válido.");
	} else {
		setSuccessFor(email);
	}

	// Comparacion del password
	if (passwordValue === "") {
		setErrorFor(password, "No puede dejar la contraseña en blanco.");
	} else if (!comprobarPassword(passwordValue)) {
		setErrorFor(password, "La contraseña debe de contener una minuscula, mayuscula, un numero y un caracter especial, con una longitud minima de 8.");
	} else {
		setSuccessFor(password);
	}

	// Comparacion del password_confirm
	if (password2Value === "") {
		setErrorFor(password2, "No puede dejar el password en blanco.");
	} else if (passwordValue !== password2Value) {
		setErrorFor(password2, "Las contraseñas no coinciden.");
	} else {
		setSuccessFor(password2);
	}

	// Comparacion del telefono
	if (telefonoValue === "") {
		setErrorFor(telefono, "No puede dejar el teléfono en blanco.");
	} else if (!comprobarTelefono(telefonoValue)) {
		setErrorFor(telefono, "El telefono debe de contener unicamente valores numericos, sin espacios o caracteres entre números.");
	} else {
		setSuccessFor(telefono);
	}

	// Comparacion del Direccion.
	if (direccionValue === "") {
		setErrorFor(direccion, "No puede dejar la dirección en blanco.");
	} else if (!comprobarDireccion(direccionValue)) {
		setErrorFor(direccion, "No ingreso una dirección válida.");
	} else {
		setSuccessFor(direccion);
	}
}

function setErrorFor(input, message) {
	const formControl = input.parentElement;
	const small = formControl.querySelector("small");
	formControl.className = "form-control error";
	small.innerText = message;
}

function setSuccessFor(input) {
	const formControl = input.parentElement;
	formControl.className = "form-control success";
}

function comprobarNombre(nombre) {
    return /^[a-zA-Záéíóú ]{3,50}$/.test(nombre);
}

function comprobarEmail(email) {
	return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@sendiit.com$/.test(email);
}

function comprobarPassword(password) {
    return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,15}$/.test(password);
}

function comprobarTelefono(telefono) {
    return /^[1-9]{2}[0-9]{8}$/.test(telefono);
}

function comprobarDireccion(direccion) {
    return /^[a-zA-Záéíóú0-9./# ]{3,80}$/.test(direccion);
}

