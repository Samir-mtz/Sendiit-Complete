const inputs = document.querySelectorAll("#formulario input");
const form = document.getElementById("formulario");
const nombre = document.getElementById("nombre");
const email = document.getElementById("email");
const password = document.getElementById("password");
const password2 = document.getElementById("password_confirm");
const telefono = document.getElementById("telefono");
const direccion = document.getElementById("direccion");

const campos = {
	email: false,
	password: false,
	nombre: false,
	password2: false,
	telefono: false,
	direccion: false,
};

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
		setErrorFor(nombre, "No puede dejar el campo de nombre en blanco.");
		campos["nombre"] = false;
	} else if (nombreValue.length < 5) {
		setErrorFor(nombre, "El nombre debe de tener una longitud mínima de 5 caracteres.");
		campos["nombre"] = false;
	} else if (nombreValue.length > 30) {
		setErrorFor(nombre, "El nombre debe de tener una longitud máxima de 30 caracteres.");
		campos["nombre"] = false;
	} else if (!comprobarNombre(nombreValue)) {
		setErrorFor(nombre, "El nombre solo puede tener letras mayusculas, minusculas y espacios.");
		campos["nombre"] = false;
	} else {
		setSuccessFor(nombre);
		campos["nombre"] = true;
	}

	// Comparacion del email
	if (emailValue === "") {
		setErrorFor(email, "No puede dejar el campo de e-mail en blanco.");
		campos["email"] = false;
	} else if (!comprobarEmail(emailValue)) {
		setErrorFor(email, "No ingreso un formato de e-mail válido.");
		campos["email"] = false;
	} else {
		setSuccessFor(email);
		campos["email"] = true;
	}

	// Comparacion del password
	if (passwordValue === "") {
		setErrorFor(password, "No puede dejar el campo de contraseña en blanco.");
		campos["password"] = false;
	} else if (passwordValue.length < 8) {
		setErrorFor(password, "La contraseña debe de tener una longitud mínima de 8 caracteres.");
		campos["password"] = false;
	} else if (passwordValue.length > 15) {
		setErrorFor(password, "La contraseña debe de tener una longitud máxima de 15 caracteres.");
		campos["password"] = false;
	} else if (!comprobarPassword(passwordValue)) {
		setErrorFor(
			password,
			"La contraseña debe de contener una minuscula, mayuscula, un numero y un caracter especial."
		);
		campos["password"] = false;
	} else {
		setSuccessFor(password);
		campos["password"] = true;
	}

	// Comparacion del password_confirm
	if (password2Value === "") {
		setErrorFor(password2, "No puede dejar el campo de confirmar contraseña en blanco.");
		campos["password2"] = false;
	} else if (passwordValue !== password2Value) {
		setErrorFor(password2, "Las contraseñas no coinciden.");
		campos["password2"] = false;
	} else {
		setSuccessFor(password2);
		campos["password2"] = true;
	}

	// Comparacion del telefono
	if (telefonoValue === "") {
		setErrorFor(telefono, "No puede dejar el campo de teléfono en blanco.");
		campos["telefono"] = false;
	}else if (telefonoValue.length !== 10) {
		setErrorFor(telefono, "El teléfono debe de tener una longitud de 10 caracteres numéricos.");
		campos["telefono"] = false;
	}else if (!comprobarTelefono(telefonoValue)) {
		setErrorFor(telefono, "El teléfono debe de contener unicamente valores numericos.");
		campos["telefono"] = false;
	} else {
		setSuccessFor(telefono);
		campos["telefono"] = true;
	}

	// Comparacion del Direccion.
	if (direccionValue === "") {
		setErrorFor(direccion, "No puede dejar el campo de dirección en blanco.");
		campos["direccion"] = false;
	}else if (direccionValue.length < 8) {
		setErrorFor(direccion, "La dirección debe de tener una longitud mínima de 8 caracteres.");
		campos["direccion"] = false;
	}else if (direccionValue.length > 40) {
		setErrorFor(direccion, "La dirección debe de tener una longitud máxima de 50 caracteres.");
		campos["direccion"] = false;
	}else if (!comprobarDireccion(direccionValue)) {
		setErrorFor(direccion, "No ingreso una dirección válida.");
		campos["direccion"] = false;
	} else {
		setSuccessFor(direccion);
		campos["direccion"] = true;
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
	return /^[a-zA-Záéíóú ]{5,30}$/.test(nombre);
}

function comprobarEmail(email) {
	return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
		email
	);
}

function comprobarPassword(password) {
	return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&-._+])[A-Za-z\d$@$!%*?&-._+]{8,15}$/.test(
		password
	);
}

function comprobarTelefono(telefono) {
	return /^[1-9]{2}[0-9]{8}$/.test(telefono);
}

function comprobarDireccion(direccion) {
	return /^[a-zA-Záéíóú0-9.,/# ]{8,40}$/.test(direccion);
}

form.addEventListener("submit", (e) => {
	e.preventDefault();
	checkInputs();
	if (
		campos.email == true &&
		campos.password == true &&
		campos.password == true &&
		campos.nombre == true &&
		campos.password2 == true &&
		campos.telefono == true &&
		campos.direccion == true
	) {
		form.submit();
	}
});
